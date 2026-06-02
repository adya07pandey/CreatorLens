import os
import re
import httpx

from app.services.transcript.youtube import (
    get_youtube_transcript
)

from app.utils.metadata import (
    normalize_metadata,
    normalize_transcript
)

def get_video_id(url):
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    if not match:
        raise Exception("Could not extract video ID")
    return match.group(1)

def parse_duration(iso):
    if not iso:
        return 0
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', iso)
    if not match:
        return 0
    h, m, s = (int(x) if x else 0 for x in match.groups())
    return h * 3600 + m * 60 + s

def get_youtube_data(url):

    video_id = get_video_id(url)

    resp = httpx.get(
        "https://www.googleapis.com/youtube/v3/videos",
        params={
            "part": "snippet,statistics,contentDetails",
            "id": video_id,
            "key": os.environ["YOUTUBE_API_KEY"]
        }
    )

    resp.raise_for_status()
    items = resp.json().get("items", [])

    if not items:
        raise Exception(f"Video not found: {video_id}")

    item = items[0]
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    content = item.get("contentDetails", {})

    raw_metadata = {
        "title": snippet.get("title"),
        "creator": snippet.get("channelTitle"),
        "views": int(stats.get("viewCount", 0)),
        "likes": int(stats.get("likeCount", 0)),
        "comments": int(stats.get("commentCount", 0)),
        "duration": parse_duration(content.get("duration")),
        "upload_date": snippet.get("publishedAt", "")[:10].replace("-", ""),
        "thumbnail": snippet.get("thumbnails", {}).get("high", {}).get("url"),
        "description": snippet.get("description"),
        "platform": "youtube"
    }

    transcript = (
        get_youtube_transcript(video_id)
        if video_id
        else []
    )

    return {
        "metadata": normalize_metadata(raw_metadata),
        "transcript": normalize_transcript(transcript)
    }