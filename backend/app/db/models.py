from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, func, BigInteger
import uuid




class Session(Base):

    __tablename__ = "sessions"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )

    url_a = Column(Text)

    url_b = Column(Text)

    anonymous_user_id = Column(
        String,
        index=True,
        nullable=False
    )

    videos = relationship(
        "Video",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    messages = relationship(
        "Message",
        back_populates="session",
        cascade="all, delete-orphan"
    )

    insights = relationship(
        "Insight",
        back_populates="session",
        uselist=False,
        cascade="all, delete-orphan"
    )


class Video(Base):

    __tablename__ = "videos"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    session_id = Column(
        String,
        ForeignKey("sessions.id"),
        index=True
    )

    video_label = Column(
        String(1),
        index=True
    )

    platform = Column(
        String,
        index=True
    )

    title = Column(Text)

    creator = Column(Text)

    followers = Column(BigInteger)

    views = Column(BigInteger)

    likes = Column(BigInteger)

    comments = Column(BigInteger)

    duration = Column(Float)

    upload_date = Column(String)

    engagement_rate = Column(Float)

    thumbnail = Column(Text)

    caption = Column(Text)

    hashtags = Column(JSONB)

    metadata_source = Column(String)

    transcript_source = Column(String)

    session = relationship(
        "Session",
        back_populates="videos"
    )

    transcript_segments = relationship(
        "TranscriptSegment",
        back_populates="video",
        cascade="all, delete-orphan"
    )


class TranscriptSegment(Base):

    __tablename__ = "transcript_segments"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    video_id = Column(
        String,
        ForeignKey("videos.id"),
        index=True
    )

    start_time = Column(Float)

    end_time = Column(Float)

    text = Column(Text)

    video = relationship(
        "Video",
        back_populates="transcript_segments"
    )


class Insight(Base):

    __tablename__ = "insights"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    session_id = Column(
        String,
        ForeignKey("sessions.id"),
        unique=True,
        index=True
    )

    hook_comparison = Column(Text)

    cta_detection = Column(JSONB)

    speech_pace = Column(JSONB)

    winning_video = Column(
        String(1)
    )

    summary = Column(Text)

    session = relationship(
        "Session",
        back_populates="insights"
    )


class Message(Base):

    __tablename__ = "messages"

    id = Column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    session_id = Column(
        String,
        ForeignKey("sessions.id"),
        index=True
    )

    role = Column(String)

    content = Column(Text)

    timestamp = Column(
        DateTime,
        server_default=func.now()
    )

    session = relationship(
        "Session",
        back_populates="messages"
    )