import httpx
import os

def download_youtube_audio(video_id, output_path):
    # Step 1: Get direct download URL (waits until ready, max 15 min videos)
    resp = httpx.get(
        f"https://ytjar.p.rapidapi.com/dl/{video_id}",
        params={
            "wait_until_the_file_is_ready": "true",
            "quality": "low"  # smaller file = faster Groq upload
        },
        headers={
            "X-RapidAPI-Key": os.environ["RAPIDAPI_KEY"],
            "X-RapidAPI-Host": "ytjar.p.rapidapi.com"
        },
        timeout=300  # up to 300s for processing
    )
    resp.raise_for_status()
    download_url = resp.json()["link"]

    # Step 2: Download the audio file
    audio_resp = httpx.get(download_url, timeout=60)
    audio_resp.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(audio_resp.content)

    return output_path