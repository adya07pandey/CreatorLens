max_words = 150
overlap_words = 30

def chunk_transcript(
    transcript,
    max_words=150,
    overlap_words=30
):

    chunks = []

    current_segments = []
    current_word_count = 0

    for segment in transcript:

        segment_words = segment["text"].split()

        current_segments.append(segment)

        current_word_count += len(segment_words)

        if current_word_count >= max_words:

            chunk_text = " ".join(
                seg["text"]
                for seg in current_segments
            )

            chunks.append({
                "text": chunk_text,
                "start_time": current_segments[0]["start"],
                "end_time": current_segments[-1]["end"]
            })

            overlap_segments = []
            overlap_count = 0

            for seg in reversed(
                current_segments
            ):

                overlap_segments.insert(
                    0,
                    seg
                )

                overlap_count += len(
                    seg["text"].split()
                )

                if overlap_count >= overlap_words:
                    break

            current_segments = overlap_segments

            current_word_count = overlap_count

    if current_segments:

        chunk_text = " ".join(
            seg["text"]
            for seg in current_segments
        )

        chunks.append({
            "text": chunk_text,
            "start_time": current_segments[0]["start"],
            "end_time": current_segments[-1]["end"]
        })

    return chunks