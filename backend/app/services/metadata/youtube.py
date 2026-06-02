import yt_dlp

from app.services.transcript.youtube import (
    get_youtube_transcript
)

from app.utils.metadata import (
    normalize_metadata,
    normalize_transcript
)


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
        "platform": "youtube"
    }

    video_id = info.get("id")

    transcript = (
        get_youtube_transcript(video_id)
        if video_id
        else []
    )

    return {
        "metadata": normalize_metadata(
            raw_metadata
        ),
        "transcript": normalize_transcript(
            transcript
        )
    }