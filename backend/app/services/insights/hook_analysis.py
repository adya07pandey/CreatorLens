def get_hook_text(transcript):

    hook_segments = []

    for segment in transcript:

        if segment["start"] <= 10:

            hook_segments.append(
                segment["text"]
            )

    return " ".join(
        hook_segments
    )