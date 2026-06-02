from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


def generate_pdf(
    filepath,
    session,
    videos,
    insight,
    messages
):

    doc = SimpleDocTemplate(
        filepath
    )

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "Video Comparison Report",
            styles["Title"]
        )
    )

    elements.append(
        Spacer(1, 12)
    )

    for video in videos:

        elements.append(
            Paragraph(
                f"Video {video.video_label}",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                f"Title: {video.title}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Creator: {video.creator}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Views: {video.views}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Likes: {video.likes}",
                styles["BodyText"]
            )
        )

        elements.append(
            Spacer(1, 10)
        )

    if insight:

        elements.append(
            Paragraph(
                "Insights",
                styles["Heading1"]
            )
        )

        elements.append(
            Paragraph(
                f"Hook Comparison: {insight.hook_comparison}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"CTA Detection: {insight.cta_detection}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Speech Pace: {insight.speech_pace}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Summary: {insight.summary}",
                styles["BodyText"]
            )
        )

    elements.append(
        Paragraph(
            "Chat History",
            styles["Heading1"]
        )
    )

    for msg in messages:

        elements.append(
            Paragraph(
                f"{msg.role}: {msg.content}",
                styles["BodyText"]
            )
        )

    doc.build(elements)