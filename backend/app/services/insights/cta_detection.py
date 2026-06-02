CTA_KEYWORDS = [
    "follow",
    "like",
    "comment",
    "share",
    "save",
    "subscribe"
]

def detect_cta(transcript):

    text = " ".join(
        segment["text"]
        for segment in transcript
    ).lower()

    found = []

    for keyword in CTA_KEYWORDS:

        if keyword in text:
            found.append(keyword)

    return found