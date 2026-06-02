def build_context(
    chunks,
    videos,
    insight
):

    context = ""

    context += "VIDEO METADATA\n\n"

    for video in videos:

        context += f"""
            Video {video.video_label}

            Title: {video.title}
            Creator: {video.creator}
            Platform: {video.platform}

            Views: {video.views}
            Likes: {video.likes}
            Comments: {video.comments}
            Followers: {video.followers}

            Duration: {video.duration}
            Engagement Rate: {video.engagement_rate}

            Caption:
            {video.caption}

            ------------------------------------

            """
    
    if insight:

        context += f"""

            VIDEO INSIGHTS

            Hook Comparison:

            {insight.hook_comparison}

            CTA Detection:

            {insight.cta_detection}

            Speech Pace:

            {insight.speech_pace}

            Winning Video:

            {insight.winning_video}

            Summary:

            {insight.summary}

            ----------------------------------

            """
        
    context += "\nVIDEO TRANSCRIPTS\n"

    for chunk in chunks:

        context += f"""

Video: {chunk["video_label"]}

Creator: {chunk["creator"]}

Timestamp:
{chunk["start_time"]} - {chunk["end_time"]}

Transcript:
{chunk["text"]}

------------------------------------

"""

    return context