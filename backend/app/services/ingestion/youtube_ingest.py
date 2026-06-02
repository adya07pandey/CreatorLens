from app.services.metadata.youtube import get_youtube_data

from app.services.transcript.downloader import download_audio
from app.services.transcript.whisper import transcribe_video
from app.utils.metadata import normalize_ingest_result, normalize_transcript

from urllib.parse import urlparse, parse_qs
import os


def clean_youtube_url(url):

    parsed = urlparse(url)

    if "/shorts/" in parsed.path:
        video_id = parsed.path.split("/shorts/")[-1].split("/")[0].split("?")[0]
        if video_id:
            return f"https://www.youtube.com/watch?v={video_id}"

    query = parse_qs(parsed.query)

    if "v" in query:
        return f"https://www.youtube.com/watch?v={query['v'][0]}"

    return url


import time

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
            "metadata_source": "ytdlp",
            "transcript_source": "ytdlp"
        })

    audio_path = None

    try:

        start = time.perf_counter()

        audio_path = download_audio(url)

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
            "metadata_source": "ytdlp",
            "transcript_source": "whisper"
        })

    finally:

        if (
            audio_path
            and
            os.path.exists(audio_path)
        ):
            os.remove(audio_path)