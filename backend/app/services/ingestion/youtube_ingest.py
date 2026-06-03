from app.services.metadata.youtube import ( get_youtube_data,  get_audio_download_url)

from app.services.transcript.downloader import (  download_audio_from_url)

from app.services.transcript.whisper import (
    transcribe_video
)

from app.utils.metadata import (
    normalize_ingest_result,
    normalize_transcript
)

from urllib.parse import (
    urlparse,
    parse_qs
)
from app.services.transcript.downloader import delete_audio_file
import os
import time


def clean_youtube_url(url):

    parsed = urlparse(url)

    if "/shorts/" in parsed.path:

        video_id = (
            parsed.path
            .split("/shorts/")[-1]
            .split("/")[0]
            .split("?")[0]
        )

        if video_id:

            return (
                f"https://www.youtube.com/watch?v={video_id}"
            )

    query = parse_qs(parsed.query)

    if "v" in query:

        return (
            f"https://www.youtube.com/watch?v={query['v'][0]}"
        )

    return url


def ingest_youtube(url):

    start_total = time.perf_counter()

    url = clean_youtube_url(url)

    start = time.perf_counter()

    data = get_youtube_data(url)

    print(
        f"[TIMING] YouTube metadata/transcript: "
        f"{time.perf_counter()-start:.2f}s"
    )

    metadata = data["metadata"]

    transcript = data["transcript"]

    if transcript:

        print(
            f"[TIMING] YouTube ingest total: "
            f"{time.perf_counter()-start_total:.2f}s"
        )

        return normalize_ingest_result({
            "metadata": metadata,
            "transcript": transcript,
            "metadata_source": "apify",
            "transcript_source": "apify"
        })

    print(
        "[INFO] No captions found. "
        "Falling back to Whisper."
    )

    audio_path = None

    try:

        start = time.perf_counter()

        video_id = data.get(
            "video_id"
        )

        if not video_id:
            raise Exception(
                "No video id found"
            )

        try:
            audio_url = get_audio_download_url(
                video_id
            )
        except Exception as e:
            raise Exception(
                f"RapidAPI audio failed: {e}"
            )
        
        audio_path = download_audio_from_url(
            audio_url
        )

        print(
            f"[TIMING] Audio download: "
            f"{time.perf_counter()-start:.2f}s"
        )

        start = time.perf_counter()

        transcript = normalize_transcript(
            transcribe_video(audio_path)
        )

        print(
            f"[TIMING] Whisper transcription: "
            f"{time.perf_counter()-start:.2f}s"
        )

        print(
            f"[TIMING] YouTube ingest total: "
            f"{time.perf_counter()-start_total:.2f}s"
        )

        return normalize_ingest_result({
            "metadata": metadata,
            "transcript": transcript,
            "metadata_source": "apify",
            "transcript_source": "whisper"
        })

    finally:

        delete_audio_file(audio_path)