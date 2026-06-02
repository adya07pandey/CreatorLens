import yt_dlp

from youtube_transcript_api import (
    YouTubeTranscriptApi
)

from app.utils.metadata import (
    normalize_metadata,
    normalize_transcript
)


def get_video_id(url):

    if "watch?v=" in url:
        return url.split("watch?v=")[1].split("&")[0]

    return None

def get_youtube_transcript(video_id):

    try:

        api = YouTubeTranscriptApi()

        transcript = api.fetch(video_id)

        return normalize_transcript(
            [
                {
                    "start": item.start,
                    "end": item.start + item.duration,
                    "text": item.text
                }
                for item in transcript
            ]
        )

    except Exception as e:

        print(
            f"Transcript API failed: {e}"
        )

        return []
    
def get_youtube_data(url):

    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

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

    video_id = info.get("id")

    transcript = (
        get_youtube_transcript(
            video_id
        )
        if video_id
        else []
    )

    return {
        "metadata": normalize_metadata(
            raw_metadata
        ),
        "transcript": transcript
    }