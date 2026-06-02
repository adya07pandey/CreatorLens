"""Normalize video metadata and transcripts so empty/None values never break downstream code."""


def safe_int(value, default=0):
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return int(value)
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def safe_float(value, default=0.0):
    if value is None or value == "":
        return default
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_str(value, default=None):
    if value is None:
        return default
    text = str(value).strip()
    return text if text else default


def safe_list(value, default=None):
    if default is None:
        default = []
    if not value or not isinstance(value, (list, tuple)):
        return list(default)
    return list(value)


def normalize_metadata(raw):
    """Return metadata with numeric fields as 0 and empty text as None or ''."""
    if not raw:
        raw = {}

    likes = safe_int(raw.get("likes", raw.get("like_count")))
    comments = safe_int(raw.get("comments", raw.get("comment_count")))
    views = safe_int(raw.get("views", raw.get("view_count")))
    duration = safe_float(raw.get("duration"))
    followers = safe_int(raw.get("followers"))

    engagement = raw.get("engagement_rate")
    if engagement is None and views > 0:
        engagement = round(((likes + comments) / views) * 100, 2)
    else:
        engagement = safe_float(engagement)

    title = safe_str(
        raw.get("title") or raw.get("caption"),
        "",
    )
    caption = safe_str(
        raw.get("caption") or raw.get("description"),
        "",
    )

    return {
        "title": title,
        "creator": safe_str(
            raw.get("creator") or raw.get("creator_name") or raw.get("uploader")
        ),
        "platform": safe_str(raw.get("platform"), "unknown"),
        "views": views,
        "likes": likes,
        "comments": comments,
        "followers": followers,
        "shares": safe_int(raw.get("shares")),
        "duration": duration,
        "upload_date": safe_str(
            raw.get("upload_date") or raw.get("timestamp")
        ),
        "thumbnail": safe_str(
            raw.get("thumbnail") or raw.get("displayUrl")
        ),
        "caption": caption,
        "description": safe_str(raw.get("description"), "") or caption,
        "hashtags": safe_list(raw.get("hashtags")),
        "engagement_rate": engagement,
    }


def normalize_transcript_segment(segment):
    if not segment:
        return None

    text = safe_str(segment.get("text"), "")
    if not text:
        return None

    return {
        "start": safe_float(segment.get("start")),
        "end": safe_float(segment.get("end")),
        "text": text,
    }


def normalize_transcript(transcript):
    if not transcript:
        return []

    if isinstance(transcript, str):
        return [{"start": 0.0, "end": 0.0, "text": transcript.strip()}]

    normalized = []
    for segment in transcript:
        item = normalize_transcript_segment(segment)
        if item:
            normalized.append(item)

    return normalized


def normalize_ingest_result(data):
    """Normalize full ingest payload (metadata + transcript)."""
    if not data:
        return data

    out = dict(data)
    out["metadata"] = normalize_metadata(data.get("metadata"))
    out["transcript"] = normalize_transcript(data.get("transcript"))
    return out
