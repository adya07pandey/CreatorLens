from app.db.database import SessionLocal

from app.db.crud import (
    get_expired_sessions,
    delete_session_by_id
)


def cleanup_sessions():

    db = SessionLocal()

    try:

        sessions = get_expired_sessions(
            db
        )

        for session in sessions:

            delete_session_by_id(
                db,
                session.id
            )

        db.commit()

    finally:

        db.close()