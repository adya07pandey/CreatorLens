import os
from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.crud import (
    get_session,
    get_session_videos,
    get_session_insight,
    get_session_messages
)

from app.services.pdf.pdf_generator import (
    generate_pdf
)

router = APIRouter()



    
@router.get(
    "/{session_id}/pdf"
)
def export_pdf(
    session_id: str,
    db: Session = Depends(get_db)
):

    os.makedirs(
        "reports",
        exist_ok=True
    )
    
    session = get_session(
        db,
        session_id
    )

    videos = get_session_videos(
        db,
        session_id
    )

    insight = get_session_insight(
        db,
        session_id
    )

    messages = get_session_messages(
        db,
        session_id
    )

    filepath = (
        f"reports/{session_id}.pdf"
    )

    generate_pdf(
        filepath,
        session,
        videos,
        insight,
        messages
    )

    return FileResponse(
        filepath,
        media_type="application/pdf",
        filename=f"{session_id}.pdf"
    )