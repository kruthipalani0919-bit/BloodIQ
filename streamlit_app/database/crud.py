"""
crud.py
Contains all database CRUD operations.
"""

from sqlalchemy.exc import SQLAlchemyError

from database.connection import Base, engine, get_session, initialize_database
from database.exceptions import DatabaseError, DatabaseOperationError
from database.models import Report, ChatMessage


def init_db():
    initialize_database()


def _raise_operation_error(operation: str, error: Exception) -> DatabaseOperationError:
    return DatabaseOperationError(
        f"Unable to {operation}. Please verify database connectivity and try again."
    )


def _format_timestamp(report) -> str:
    timestamp = report.created_at or getattr(report, "updated_at", None)
    if timestamp:
        return timestamp.strftime("%b %d, %Y · %I:%M %p")
    return "Unknown"


def save_report(report_text: str) -> int:
    try:
        with get_session() as session:
            report = Report(report_text=report_text)
            session.add(report)
            session.flush()
            return report.id
    except DatabaseError as error:
        raise _raise_operation_error("save the report", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("save the report", error) from error


def update_analysis(report_id: int, extracted_values: str):
    try:
        with get_session() as session:
            report = session.query(Report).filter(Report.id == report_id).first()

            if report:
                report.extracted_values = extracted_values
    except DatabaseError as error:
        raise _raise_operation_error("update the analysis", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("update the analysis", error) from error


def update_diet(report_id: int, diet_plan: str):
    try:
        with get_session() as session:
            report = session.query(Report).filter(Report.id == report_id).first()

            if report:
                report.diet_plan = diet_plan
    except DatabaseError as error:
        raise _raise_operation_error("update the diet plan", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("update the diet plan", error) from error


def save_message(report_id: int, role: str, content: str):
    try:
        with get_session() as session:
            session.add(
                ChatMessage(
                    report_id=report_id,
                    role=role,
                    content=content
                )
            )
    except DatabaseError as error:
        raise _raise_operation_error("save the chat message", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("save the chat message", error) from error


def get_chat_history(report_id: int):
    try:
        with get_session() as session:
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
    except DatabaseError as error:
        raise _raise_operation_error("load the chat history", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("load the chat history", error) from error


def get_all_reports():
    try:
        with get_session() as session:
            reports = (
                session.query(Report)
                .order_by(Report.created_at.desc())
                .all()
            )

            return [
                {
                    "id": report.id,
                    "created_at": _format_timestamp(report),
                    "preview": (report.report_text[:60].replace("\n", " ") + "...")
                    if report.report_text else "...",
                    "has_diet": report.diet_plan is not None,
                    "has_analysis": report.extracted_values is not None,
                }
                for report in reports
            ]
    except DatabaseError as error:
        raise _raise_operation_error("load reports", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("load reports", error) from error


def get_report_by_id(report_id: int):
    try:
        with get_session() as session:
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
    except DatabaseError as error:
        raise _raise_operation_error("load the report", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("load the report", error) from error


def delete_report(report_id: int):
    try:
        with get_session() as session:
            report = (
                session.query(Report)
                .filter(Report.id == report_id)
                .first()
            )

            if report:
                session.delete(report)
    except DatabaseError as error:
        raise _raise_operation_error("delete the report", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("delete the report", error) from error