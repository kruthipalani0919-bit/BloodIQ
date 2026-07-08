"""
crud.py
Contains all database CRUD operations.
"""

from database.connection import SessionLocal, Base, engine
from database.models import Report, ChatMessage


def init_db():
    Base.metadata.create_all(engine)


def save_report(report_text: str) -> int:
    session = SessionLocal()
    try:
        report = Report(report_text=report_text)
        session.add(report)
        session.commit()
        session.refresh(report)
        return report.id
    finally:
        session.close()


def update_analysis(report_id: int, extracted_values: str):
    session = SessionLocal()
    try:
        report = session.query(Report).filter(Report.id == report_id).first()

        if report:
            report.extracted_values = extracted_values
            session.commit()
    finally:
        session.close()


def update_diet(report_id: int, diet_plan: str):
    session = SessionLocal()
    try:
        report = session.query(Report).filter(Report.id == report_id).first()

        if report:
            report.diet_plan = diet_plan
            session.commit()
    finally:
        session.close()


def save_message(report_id: int, role: str, content: str):
    session = SessionLocal()
    try:
        session.add(
            ChatMessage(
                report_id=report_id,
                role=role,
                content=content
            )
        )
        session.commit()
    finally:
        session.close()


def get_chat_history(report_id: int):
    session = SessionLocal()

    try:
        messages = (
            session.query(ChatMessage)
            .filter(ChatMessage.report_id == report_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )

        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]

    finally:
        session.close()


def get_all_reports():
    session = SessionLocal()

    try:
        reports = (
            session.query(Report)
            .order_by(Report.created_at.desc())
            .all()
        )

        return [
            {
                "id": report.id,
                "created_at": report.created_at.strftime("%b %d, %Y · %I:%M %p"),
                "preview": report.report_text[:60].replace("\n", " ") + "...",
                "has_diet": report.diet_plan is not None,
                "has_analysis": report.extracted_values is not None,
            }
            for report in reports
        ]

    finally:
        session.close()


def get_report_by_id(report_id: int):
    session = SessionLocal()

    try:
        report = (
            session.query(Report)
            .filter(Report.id == report_id)
            .first()
        )

        if not report:
            return None

        return {
            "id": report.id,
            "report_text": report.report_text,
            "extracted_values": report.extracted_values,
            "diet_plan": report.diet_plan,
        }

    finally:
        session.close()


def delete_report(report_id: int):
    session = SessionLocal()

    try:
        report = (
            session.query(Report)
            .filter(Report.id == report_id)
            .first()
        )

        if report:
            session.delete(report)
            session.commit()

    finally:
        session.close()