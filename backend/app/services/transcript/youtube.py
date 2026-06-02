from youtube_transcript_api import YouTubeTranscriptApi

def get_youtube_transcript(video_id, url=None):
    try:
        api = YouTubeTranscriptApi()
        transcript = api.fetch(
            video_id,
            languages=["en", "en-US", "en-GB"]
        )

        if transcript:
            return [
                {
                    "start": entry.start,
                    "end": entry.start + entry.duration,
                    "text": entry.text
                }
                for entry in transcript
            ]
    except Exception as e:
        print(f"YouTube transcript failed: {e}")

 