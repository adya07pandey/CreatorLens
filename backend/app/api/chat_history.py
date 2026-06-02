from fastapi import APIRouter
from fastapi import Depends

from app.db.database import get_db
from app.db.crud import get_session_messages

router = APIRouter()

@router.get("/{session_id}")
def get_chat_history(
    session_id,
    db=Depends(get_db)
):

    messages = get_session_messages(
        db,
        session_id
    )

    return [
        {
            "role": m.role,
            "content": m.content,
            "timestamp": m.timestamp
        }
        for m in messages
    ]