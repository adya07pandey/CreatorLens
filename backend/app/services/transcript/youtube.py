from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable
)


def get_youtube_transcript(video_id):

    try:

        transcript = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=["en", "en-US", "en-GB"]
        )

        return [
            {
                "start": entry["start"],
                "end": entry["start"] + entry["duration"],
                "text": entry["text"]
            }
            for entry in transcript
        ]

    except (
        NoTranscriptFound,
        TranscriptsDisabled,
        VideoUnavailable
    ):

        return []

    except Exception as e:

        print(f"YouTube transcript failed: {e}")

        return []