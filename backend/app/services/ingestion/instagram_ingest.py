from app.services.metadata.instagram_apify import get_reel_data, extract_apify_metadata
from app.services.metadata.instagram_ytdlp import get_instagram_metadata_ytdlp
from app.services.transcript.downloader import delete_audio_file
from app.services.transcript.instagram_ytdlp import get_ytdlp_transcript
from app.services.transcript.whisper import transcribe_video
from app.services.transcript.downloader import download_audio
from app.utils.metadata import normalize_ingest_result, normalize_transcript

import os
import time

def ingest_instagram(url):
    start_total = time.perf_counter()
    try:

        start = time.perf_counter()

        item = get_reel_data(url)

        print(
            f"[TIMING] Apify reel scraper: "
            f"{time.perf_counter()-start:.2f}s"
        )

        metadata = extract_apify_metadata(item)

        transcript = item.get("transcript", "")

        if not transcript:
            raise Exception("Transcript missing")

    

        transcript = [
            {
                "start": 0.0,
                "end": metadata.get("duration", 0),
                "text": transcript
            }
        ]

        return normalize_ingest_result({
            "metadata": metadata,
            "transcript": normalize_transcript(transcript),
            "metadata_source": "apify",
            "transcript_source": "apify"
        })
    
    except Exception as e:

        print(f"Apify failed: {e}")



    start = time.perf_counter()

    metadata = get_instagram_metadata_ytdlp(
        url
    )

    print(
        f"[TIMING] yt-dlp metadata: "
        f"{time.perf_counter()-start:.2f}s"
    )
    


    try:

        start = time.perf_counter()

        transcript = get_ytdlp_transcript(url)

        print(
            f"[TIMING] yt-dlp transcript: "
            f"{time.perf_counter()-start:.2f}s"
        )
        transcript = [
            {
                "start": 0.0,
                "end": metadata.get("duration", 0),
                "text": transcript
            }
        ]

        return normalize_ingest_result({
            "metadata": metadata,
            "transcript": normalize_transcript(transcript),
            "metadata_source": "ytdlp",
            "transcript_source": "ytdlp"
        })

    except Exception as e:

        print(f"yt-dlp transcript failed: {e}")


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
            f"[TIMING] Instagram ingest total: "
            f"{time.perf_counter()-start_total:.2f}s"
        )
        return normalize_ingest_result({
            "metadata": metadata,
            "transcript": transcript,
            "metadata_source": "ytdlp",
            "transcript_source": "whisper"
        })
        

    finally:

        delete_audio_file(audio_path)
