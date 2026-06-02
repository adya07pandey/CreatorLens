from app.utils.metadata import safe_float


def calculate_speech_pace(
    transcript,
    duration_seconds
):

    total_words = 0

    for segment in transcript or []:

        text = (segment or {}).get("text") or ""
        total_words += len(text.split())

    duration_seconds = safe_float(duration_seconds)

    if duration_seconds <= 0:
        return 0

    duration_minutes = duration_seconds / 60

    if duration_minutes <= 0:
        return 0

    return round(
        total_words /
        duration_minutes,
        2
    )