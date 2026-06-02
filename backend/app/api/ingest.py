from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

import asyncio
import re
import time

from app.schemas.schemas import IngestRequest

from app.db.database import get_db

from app.db.crud import (
    create_session,
    create_video,
    create_transcript_segments,
    create_insight,
    create_message,
    save_message,
    count_today_sessions
)

from app.services.ingestion.instagram_ingest import ingest_instagram
from app.services.ingestion.youtube_ingest import ingest_youtube

from app.services.insights.hook_analysis import ( get_hook_text)

from app.services.insights.cta_detection import ( detect_cta )

from app.services.insights.speech_pace import ( calculate_speech_pace )

from app.utils.chunker import ( chunk_transcript )

from app.services.vectorstore.qdrant import ( store_chunks)

from app.services.llm.prompts import build_hook_prompt

from app.services.insights.summary import generate_comparison_summary
import os, psutil

def log_ram(stage):
    process = psutil.Process(os.getpid())
    print(
        f"[RAM] {stage}: "
        f"{process.memory_info().rss / 1024 / 1024:.2f} MB"
    )
router = APIRouter()

ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


def clean_error_message(error):
    message = ANSI_ESCAPE_RE.sub("", str(error)).strip()

    if message.startswith("ERROR:"):
        message = message[len("ERROR:"):].strip()

    message = re.sub(r"^\[[^\]]+\]\s+[^:]+:\s*", "", message).strip()

    return message or "Ingestion failed"


def get_platform(url):

    if "instagram.com" in url:
        return "instagram"

    if (
        "youtube.com" in url
        or
        "youtu.be" in url
    ):
        return "youtube"

    raise ValueError(
        f"Unsupported URL: {url}"
    )


def process_url(url):
    platform = get_platform(url)

    if platform == "instagram":
        return ingest_instagram(url)

    if platform == "youtube":
        return ingest_youtube(url)

    raise ValueError(
        f"Unsupported platform: {platform}"
    )


@router.post("/ingest")
async def ingest(
    body: IngestRequest,
    db: Session = Depends(get_db)
):
    count = count_today_sessions(
                db,
                body.user_id
            )

    if count >= 5:

        raise HTTPException(
                    status_code=429,
                    detail="Daily session limit reached"
                )
    try:
        log_ram("start")
        t0 = time.perf_counter()
        result_a, result_b = await asyncio.gather(
            asyncio.to_thread(
                process_url,
                body.url_a
            ),
            asyncio.to_thread(
                process_url,
                body.url_b
            ),
            return_exceptions=True
        )

        if isinstance(
            result_a,
            Exception
        ):
            print(
                "Error processing URL A:",
                type(result_a).__name__,
                str(result_a)[:300],
                flush=True,
            )
            log_ram("video A")
            return {
                "success": False,
                "failed_video": "A",
                "error": clean_error_message(result_a)
            }
        log_ram("video A")
        if isinstance(
            result_b,
            Exception
        ):
            print(
                "Error processing URL B:",
                type(result_b).__name__,
                str(result_b)[:300],
                flush=True,
            )
            log_ram("video B")
            return {
                "success": False,
                "failed_video": "B",
                "error": clean_error_message(result_b)
            }
        print(
            f"[TIMING] video processing: "
            f"{time.perf_counter()-t0:.2f}s"
        )
        log_ram("video B")
        try:
            
            session = create_session(
                db=db,
                user_id=body.user_id,
                url_a=body.url_a,
                url_b=body.url_b
            )

            video_a = create_video(
                db=db,
                session_id=session.id,
                video_label="A",
                data=result_a
            )

            create_transcript_segments(
                db=db,
                video_id=video_a.id,
                transcript=result_a[
                    "transcript"
                ]
            )
            log_ram("transcription A")
            video_b = create_video(
                db=db,
                session_id=session.id,
                video_label="B",
                data=result_b
            )

            create_transcript_segments(
                db=db,
                video_id=video_b.id,
                transcript=result_b[
                    "transcript"
                ]
            )
            log_ram("transcription b")
            hook_a = get_hook_text(
                result_a["transcript"]
            )

            hook_b = get_hook_text(
                result_b["transcript"]
            )

            hook_comparison = build_hook_prompt(
                hook_a,
                hook_b
            )

            cta_a = detect_cta(
                result_a["transcript"]
            )

            cta_b = detect_cta(
                result_b["transcript"]
            )

            speech_a = calculate_speech_pace(
                result_a["transcript"],
                result_a["metadata"]["duration"]
            )

            speech_b = calculate_speech_pace(
                result_b["transcript"],
                result_b["metadata"]["duration"]
            )
            t1 = time.perf_counter()
            summary = generate_comparison_summary(

                metadata_a=result_a["metadata"],
                metadata_b=result_b["metadata"],

                hook_comparison=hook_comparison,

                cta_a=cta_a,
                cta_b=cta_b,

                speech_a=speech_a,
                speech_b=speech_b
            )
            log_ram("summary")
            print(
                f"[TIMING] summary generation: "
                f"{time.perf_counter()-t1:.2f}s"
            )
            t2 = time.perf_counter()
            create_insight(
                db=db,
                session_id=session.id,

                hook_comparison=
                    hook_comparison,

                cta_detection={
                    "video_a": cta_a,
                    "video_b": cta_b
                },

                speech_pace={
                    "video_a": speech_a,
                    "video_b": speech_b
                },

                winning_video=None,

                summary=summary
            )


            save_message(
                db=db,
                session_id=session.id,
                role="assistant",
                content=summary
            )
            
            db.commit()
            print(
                f"[TIMING] postgres save: "
                f"{time.perf_counter()-t2:.2f}s"
            )
        except Exception:

            db.rollback()

            raise

        try:
            t3 = time.perf_counter()
            chunks_a = chunk_transcript(
                result_a["transcript"]
            )

            chunks_b = chunk_transcript(
                result_b["transcript"]
            )

            store_chunks(
                chunks=chunks_a,
                session_id=session.id,
                video_label="A",
                creator=result_a[
                    "metadata"
                ]["creator"],
                platform=result_a[
                    "metadata"
                ]["platform"]
            )

            store_chunks(
                chunks=chunks_b,
                session_id=session.id,
                video_label="B",
                creator=result_b[
                    "metadata"
                ]["creator"],
                platform=result_b[
                    "metadata"
                ]["platform"]
            )
            print(
                f"[TIMING] qdrant store: "
                f"{time.perf_counter()-t3:.2f}s"
            )
        except Exception as e:

            print(
                f"Qdrant Error: {e}"
            )

        print(
            f"[TIMING] ingest completed in {time.perf_counter() - t0:.2f}s "
            f"session_id={session.id}",
            flush=True
        )

        return {
            "success": True,
            "session_id": session.id
        }

    except HTTPException:
        raise

    except SQLAlchemyError as e:
        elapsed = time.perf_counter() - t0 if "t0" in locals() else -1
        print(
            f"[TIMING] ingest database failed in {elapsed:.2f}s error={str(e)[:500]}",
            flush=True
        )
        raise HTTPException(
            status_code=503,
            detail="Database connection failed. Please try again."
        )

    except Exception as e:

        elapsed = time.perf_counter() - t0 if "t0" in locals() else -1
        print(
            f"[TIMING] ingest failed in {elapsed:.2f}s error={str(e)[:200]}",
            flush=True
        )
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
