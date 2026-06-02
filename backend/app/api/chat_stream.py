from fastapi import APIRouter
from fastapi import Depends
import json
import time
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from app.schemas.schemas import ChatRequest

from app.db.database import get_db

from app.db.crud import save_message

from app.graph.workflow import workflow

from app.services.llm.qwen import stream_qwen

router = APIRouter()


@router.post("/chat/stream")
async def chat_stream(
    body: ChatRequest,
    db: Session = Depends(get_db)
):
    t0 = time.perf_counter()

    save_message(
        db=db,
        session_id=body.session_id,
        role="user",
        content=body.message
    )

    db.commit()

    result = workflow.invoke(
        {
            "session_id": body.session_id,
            "query": body.message
        }
    )

    prompt = result["prompt"]

    async def event_generator():

        full_answer = ""

        try:

            buffer = ""

            for token in stream_qwen(prompt):

                full_answer += token
                buffer += token

                if len(buffer) >= 20:

                    payload = {
                        "type": "token",
                        "token": buffer
                    }

                    yield f"data: {json.dumps(payload)}\n\n"

                    buffer = ""

            if buffer:

                payload = {
                    "type": "token",
                    "token": buffer
                }

                yield f"data: {json.dumps(payload)}\n\n"

            save_message(
                db=db,
                session_id=body.session_id,
                role="assistant",
                content=full_answer
            )

            db.commit()

            print(
                f"[TIMING] chat_stream completed in {time.perf_counter() - t0:.2f}s "
                f"session_id={body.session_id} chars={len(full_answer)}",
                flush=True
            )

            payload = {
                "type": "sources",
                "sources": result["sources"]
            }

            yield f"data: {json.dumps(payload)}\n\n"

            payload = {
                "type": "done"
            }

            yield f"data: {json.dumps(payload)}\n\n"

        except Exception as e:

            print(
                f"[TIMING] chat_stream failed in {time.perf_counter() - t0:.2f}s "
                f"session_id={body.session_id} error={str(e)[:200]}",
                flush=True
            )
            payload = {
                "type": "error",
                "message": str(e)
            }

            yield f"data: {json.dumps(payload)}\n\n"
            
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )