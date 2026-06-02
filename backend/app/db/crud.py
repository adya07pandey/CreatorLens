from app.db.models import (
    Session,
    Video,
    TranscriptSegment,
    Insight,
    Message
)
from datetime import date
from sqlalchemy import func
from app.services.vectorstore.qdrant import (
    delete_session_chunks
)
from app.utils.metadata import normalize_metadata, normalize_transcript
from datetime import datetime
from datetime import timedelta

def create_session(
    db,
    user_id,
    url_a,
    url_b
):

    session = Session(
        anonymous_user_id=user_id,
        url_a=url_a,
        url_b=url_b
    )

    db.add(session)

    db.flush()

    return session


def create_video(
    db,
    session_id,
    video_label,
    data
):

    metadata = normalize_metadata(data.get("metadata"))
    data["metadata"] = metadata
    data["transcript"] = normalize_transcript(data.get("transcript"))

    video = Video(
        session_id=session_id,

        video_label=video_label,

        platform=metadata.get(
            "platform"
        ),

        title=metadata.get(
            "title"
        ),

        creator=metadata.get(
            "creator"
        ),

        followers=metadata["followers"],

        views=metadata["views"],

        likes=metadata["likes"],

        comments=metadata["comments"],

        duration=metadata["duration"],

        upload_date=metadata.get(
            "upload_date"
        ),

        engagement_rate=metadata["engagement_rate"],

        thumbnail=metadata.get(
            "thumbnail"
        ),

        caption=metadata.get(
            "caption"
        ),

        hashtags=metadata["hashtags"],

        metadata_source=data.get(
            "metadata_source"
        ),

        transcript_source=data.get(
            "transcript_source"
        )
    )

    db.add(video)

    db.flush()

    return video


def create_transcript_segments(
    db,
    video_id,
    transcript
):

    segments = []

    for segment in transcript:

        transcript_segment = TranscriptSegment(
            video_id=video_id,

            start_time=segment.get(
                "start"
            ),

            end_time=segment.get(
                "end"
            ),

            text=segment.get(
                "text"
            )
        )

        db.add(
            transcript_segment
        )

        segments.append(
            transcript_segment
        )

    db.flush()

    return segments


def create_insight(
    db,
    session_id,
    hook_comparison,
    cta_detection,
    speech_pace,
    winning_video,
    summary
):

    insight = Insight(
        session_id=session_id,

        hook_comparison=
            hook_comparison,

        cta_detection=
            cta_detection,

        speech_pace=
            speech_pace,

        winning_video=
            winning_video,

        summary=
            summary
    )

    db.add(insight)

    db.flush()

    return insight


def create_message(
    db,
    session_id,
    role,
    content
):

    message = Message(
        session_id=session_id,
        role=role,
        content=content
    )

    db.add(message)

    db.flush()

    return message


def save_message(
    db,
    session_id,
    role,
    content
):

    message = Message(
        session_id=session_id,

        role=role,

        content=content
    )

    db.add(message)

    db.flush()

    return message


def get_session(
    db,
    session_id
):

    return (
        db.query(Session)
        .filter(
            Session.id == session_id
        )
        .first()
    )


def get_user_sessions(
    db,
    user_id
):

    return db.query(
        Session
    ).filter(
        Session.anonymous_user_id == user_id
    ).order_by(
        Session.created_at.desc()
    ).all()


def get_session_messages(
    db,
    session_id
):

    return (
        db.query(Message)
        .filter(
            Message.session_id
            == session_id
        )
        .order_by(
            Message.timestamp.asc()
        )
        .all()
    )


def delete_session_by_id(
    db,
    session_id
):

    session = db.query(
        Session
    ).filter(
        Session.id == session_id
    ).first()

    if not session:
        return False

    try:

        delete_session_chunks(
            session_id
        )

    except Exception as e:

        print(
            f"Qdrant delete failed: {e}"
        )

    db.delete(session)

    return True


def get_session_videos(
    db,
    session_id
):

    videos = db.query(
        Video
    ).filter(
        Video.session_id == session_id
    ).all()

    return videos


def get_session_insight(
    db,
    session_id
):

    return db.query(
        Insight
    ).filter(
        Insight.session_id == session_id
    ).first()


def count_today_sessions(
    db,
    user_id
):

    return db.query(
        Session
    ).filter(
        Session.anonymous_user_id == user_id
    ).filter(
        func.date(
            Session.created_at
        ) == date.today()
    ).count()


def get_expired_sessions(
    db
):

    cutoff = (
        datetime.utcnow()
        - timedelta(days=7)
    )

    return (
        db.query(Session)
        .filter(
            Session.created_at < cutoff
        )
        .all()
    )