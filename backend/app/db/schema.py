"""SQLAlchemy ORM models. Mirrors the schema in the v1 plan.

Tables: users, sessions, turns, editor_events, scores, corpus_chunks.
The `sessions` table's class is named `InterviewSession` to avoid clashing
with `sqlalchemy.orm.Session` in code.
"""
from __future__ import annotations

import uuid
from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models."""


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    clerk_id: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), index=True)
    target_companies: Mapped[list[str]] = mapped_column(JSONB, default=list)
    target_role: Mapped[str | None] = mapped_column(String(64), default=None)
    resume_text: Mapped[str | None] = mapped_column(Text, default=None)
    resume_extracted: Mapped[dict | None] = mapped_column(JSONB, default=None)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    sessions: Mapped[list[InterviewSession]] = relationship(back_populates="user")


class InterviewSession(Base):
    """A single mock-interview session."""

    __tablename__ = "sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    interview_type: Mapped[str] = mapped_column(String(32))
    # ^ dsa | system_design | behavioral | mixed
    target_company: Mapped[str | None] = mapped_column(String(64))
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    ended_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    audio_url: Mapped[str | None] = mapped_column(Text)  # R2 path to full session audio

    user: Mapped[User] = relationship(back_populates="sessions")
    turns: Mapped[list[Turn]] = relationship(
        back_populates="session", order_by="Turn.t_ms"
    )
    editor_events: Mapped[list[EditorEvent]] = relationship(
        back_populates="session", order_by="EditorEvent.t_ms"
    )
    scores: Mapped[list[Score]] = relationship(back_populates="session")


class Turn(Base):
    __tablename__ = "turns"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id"), index=True)
    speaker: Mapped[str] = mapped_column(String(16))  # user | bot
    text: Mapped[str] = mapped_column(Text)
    audio_url: Mapped[str | None] = mapped_column(Text)
    t_ms: Mapped[int] = mapped_column(Integer)
    duration_ms: Mapped[int | None] = mapped_column(Integer)

    session: Mapped[InterviewSession] = relationship(back_populates="turns")


class EditorEvent(Base):
    __tablename__ = "editor_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id"), index=True)
    type: Mapped[str] = mapped_column(String(32))
    # ^ keystroke | paste | tab_switch | focus_loss | code_run
    payload: Mapped[dict] = mapped_column(JSONB)
    t_ms: Mapped[int] = mapped_column(Integer)

    session: Mapped[InterviewSession] = relationship(back_populates="editor_events")


class Score(Base):
    __tablename__ = "scores"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("sessions.id"), index=True)
    criterion: Mapped[str] = mapped_column(String(64))
    # ^ technical_correctness | process | structure | clarity | confidence | code_process
    score: Mapped[float] = mapped_column()
    rationale: Mapped[str] = mapped_column(Text)
    evidence: Mapped[dict] = mapped_column(JSONB, default=dict)
    model_version: Mapped[str] = mapped_column(String(64))
    # ^ ft-qwen2.5-7b-v1 | haiku-zeroshot | etc.

    session: Mapped[InterviewSession] = relationship(back_populates="scores")


class CorpusChunk(Base):
    __tablename__ = "corpus_chunks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    text: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(Vector(768))  # bge-base-en-v1.5
    company: Mapped[str | None] = mapped_column(String(64), index=True)
    role: Mapped[str | None] = mapped_column(String(64), index=True)
    round_type: Mapped[str | None] = mapped_column(String(32), index=True)
    year: Mapped[int | None] = mapped_column(Integer, index=True)
    source_url: Mapped[str] = mapped_column(Text)
    source_name: Mapped[str] = mapped_column(String(64))
    # ^ reddit | gfg | leetcode_discuss | interviewbit
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
