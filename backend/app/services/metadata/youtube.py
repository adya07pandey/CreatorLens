import os
import yt_dlp
import webvtt

from app.utils.metadata import normalize_metadata, normalize_transcript

TEMP_DIR = "temp"

os.makedirs(TEMP_DIR, exist_ok=True)



def parse_vtt(video_id):

    files = os.listdir(TEMP_DIR)

    vtt_file = next(
        (
            f
            for f in files
            if f.startswith(video_id)
            and f.endswith(".vtt")
        ),
        None
    )

    if not vtt_file:
        return None

    path = os.path.join(TEMP_DIR, vtt_file)

    transcript = []

    try:

        for caption in webvtt.read(path):

            text = caption.text.strip()

            if not text:
                continue

            transcript.append({
                "start": caption.start,
                "end": caption.end,
                "text": text
            })

    finally:

        if os.path.exists(path):
            os.remove(path)

    if not transcript:
        return None

    return normalize_transcript(transcript)


def get_youtube_data(url):

    ydl_opts = {
        "skip_download": True,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitlesformat": "vtt",
        "outtmpl": f"{TEMP_DIR}/%(id)s.%(ext)s",
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

        video_id = info["id"]

        try:
            ydl.download([url])
            transcript = parse_vtt(video_id)
        except Exception:
            transcript = None

    raw_metadata = {
        "title": info.get("title"),
        "creator": info.get("uploader"),
        "views": info.get("view_count"),
        "likes": info.get("like_count"),
        "comments": info.get("comment_count"),
        "duration": info.get("duration"),
        "upload_date": info.get("upload_date"),
        "thumbnail": info.get("thumbnail"),
        "description": info.get("description"),
        "platform": "youtube",
    }

    return {
        "metadata": normalize_metadata(raw_metadata),
        "transcript": transcript or [],
    }
