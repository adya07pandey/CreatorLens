import os
import yt_dlp
import webvtt

TEMP_DIR = "temp"

os.makedirs(TEMP_DIR, exist_ok=True)

def timestamp_to_seconds(timestamp):

    h, m, s = timestamp.split(":")

    return (
        int(h) * 3600
        + int(m) * 60
        + float(s)
    )

def parse_vtt(video_id):

    files = os.listdir(TEMP_DIR)

    vtt_file = next(
        (
            f for f in files
            if f.startswith(video_id)
            and f.endswith(".vtt")
        ),
        None
    )

    if not vtt_file:
        raise Exception("Subtitle file not found")

    path = os.path.join(
        TEMP_DIR,
        vtt_file
    )

    transcript = []

    try:

        for caption in webvtt.read(path):

            text = caption.text.strip()

            if not text:
                continue

            transcript.append({
                "start": timestamp_to_seconds(caption.start),
                "end": timestamp_to_seconds(caption.end),
                "text": text
            })

    finally:

        if os.path.exists(path):
            os.remove(path)

    if not transcript:
        raise Exception("No transcript found")

    return transcript


def get_youtube_transcript(url):

    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en"],
        "subtitlesformat": "vtt",
        "outtmpl": f"{TEMP_DIR}/%(id)s.%(ext)s",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

        video_id = info["id"]

        ydl.download([url])

    return parse_vtt(video_id)