"""
models.py
Contains all SQLAlchemy ORM models.
"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import relationship

from database.connection import Base


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        Index("ix_reports_created_at", "created_at"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    report_text = Column(Text, nullable=False)
    extracted_values = Column(Text)
    diet_plan = Column(Text)

    messages = relationship(
        "ChatMessage",
        back_populates="report",
        cascade="all, delete-orphan"
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    __table_args__ = (
        Index("ix_chat_messages_report_id", "report_id"),
        Index("ix_chat_messages_created_at", "created_at"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    report_id = Column(
        Integer,
        ForeignKey("reports.id"),
        nullable=False
    )

    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    report = relationship(
        "Report",
        back_populates="messages"
    )