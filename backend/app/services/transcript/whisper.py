from faster_whisper import WhisperModel


model = WhisperModel(
    "base",
    device="cpu",
    compute_type="int8"
)



def transcribe_video(audio_path):

    segments, info = model.transcribe(
        audio_path
    )

    transcript = []

    for segment in segments:

        transcript.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })

    return transcript
