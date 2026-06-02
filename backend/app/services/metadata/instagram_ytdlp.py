import yt_dlp

from app.utils.metadata import normalize_metadata


def get_instagram_metadata_ytdlp(
    url
):

    ydl_opts = {
        "quiet": True
    }

    with yt_dlp.YoutubeDL(
        ydl_opts
    ) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

    raw = {
        "title": info.get("title"),
        "caption": info.get("description"),
        "creator": info.get("uploader"),
        "views": info.get("view_count"),
        "likes": info.get("like_count"),
        "duration": info.get("duration"),
        "platform": "instagram",
    }

    return normalize_metadata(raw)
