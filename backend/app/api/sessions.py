from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.db.crud import (
    get_user_sessions,
    get_session,
    delete_session_by_id,
    get_session_messages,
    get_session_videos
)

router = APIRouter()

def _video_payload(video):
    if not video:
        return None

    return {
        "label": video.video_label,
        "title": video.title,
        "creator": video.creator,
        "thumbnail": video.thumbnail,
        "views": video.views,
        "likes": video.likes,
        "comments": video.comments,
        "duration": video.duration,
        "platform": video.platform
    }

@router.get("/")
def list_sessions(
    user_id: str,
    db: Session = Depends(get_db)
):

    sessions = get_user_sessions(
        db,
        user_id
    )

    result = []

    for s in sessions:
        videos = get_session_videos(
            db,
            s.id
        )

        by_label = {
            v.video_label: v
            for v in videos
        }

        va = by_label.get("A")
        vb = by_label.get("B")

        title_a = (
            va.title
            if va and va.title
            else None
        ) or "Video A"

        title_b = (
            vb.title
            if vb and vb.title
            else None
        ) or "Video B"

        result.append(
            {
                "id": s.id,
                "created_at": s.created_at,
                "title_a": title_a,
                "title_b": title_b,
                "label": f"{title_a} vs {title_b}"
            }
        )

    return result


@router.get("/session/{session_id}/details")
def get_session_details(
    session_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):

    session = get_session(
        db,
        session_id
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    if (
        session.anonymous_user_id
        != user_id
    ):

        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    videos = get_session_videos(
        db,
        session_id
    )

    by_label = {
        v.video_label: v
        for v in videos
    }

    return {
        "session_id": session_id,
        "url_a": session.url_a,
        "url_b": session.url_b,
        "video_a": _video_payload(by_label.get("A")),
        "video_b": _video_payload(by_label.get("B"))
    }

# @router.get("/{session_id}")
# def get_session_details(
#     session_id: str,
#     user_id: str,
#     db: Session = Depends(get_db)
# ):

#     session = get_session(
#         db,
#         session_id
#     )

#     if not session:

#         raise HTTPException(
#             status_code=404,
#             detail="Session not found"
#         )

#     if (
#         session.anonymous_user_id
#         != user_id
#     ):

#         raise HTTPException(
#             status_code=403,
#             detail="Forbidden"
#         )

#     return {
#         "id": session.id,
#         "created_at": session.created_at
#     }


@router.get("/{session_id}")
def get_messages(
    session_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):

    session = get_session(
        db,
        session_id
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    if (
        session.anonymous_user_id
        != user_id
    ):

        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    messages = get_session_messages(
        db,
        session_id
    )

    return {
        "session_id": session_id,
        "messages": [
            {
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.timestamp
            }
            for msg in messages
        ]
    }


@router.delete("/{session_id}")
def remove_session(
    session_id: str,
    user_id: str,
    db: Session = Depends(get_db)
):

    session = get_session(
        db,
        session_id
    )

    if not session:

        raise HTTPException(
            status_code=404,
            detail="Session not found"
        )

    if (
        session.anonymous_user_id
        != user_id
    ):

        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    success = delete_session_by_id(
        db,
        session_id
    )

    db.commit()

    return {
        "success": success
    }