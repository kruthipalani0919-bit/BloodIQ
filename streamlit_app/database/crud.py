from sqlalchemy.exc import SQLAlchemyError
from database.connection import get_session, initialize_database
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


def _verify_report_ownership(session, report_id: int, user_id: int | None) -> bool:
    if user_id is None:
        return session.query(Report).filter(Report.id == report_id, Report.user_id.is_(None)).first() is not None
    return session.query(Report).filter(Report.id == report_id, Report.user_id == user_id).first() is not None


def save_report(report_text: str, user_id: int | None = None) -> int:
    try:
        with get_session() as session:
            report = Report(report_text=report_text, user_id=user_id)
            session.add(report)
            session.flush()
            return report.id
    except DatabaseError as error:
        raise _raise_operation_error("save the report", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("save the report", error) from error


def update_analysis(report_id: int, extracted_values: str, user_id: int | None = None):
    try:
        with get_session() as session:
            query = session.query(Report).filter(Report.id == report_id)
            if user_id is not None:
                query = query.filter(Report.user_id == user_id)
            else:
                query = query.filter(Report.user_id.is_(None))
            report = query.first()

            if report:
                report.extracted_values = extracted_values
    except DatabaseError as error:
        raise _raise_operation_error("update the analysis", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("update the analysis", error) from error


def update_diet(report_id: int, diet_plan: str, user_id: int | None = None):
    try:
        with get_session() as session:
            query = session.query(Report).filter(Report.id == report_id)
            if user_id is not None:
                query = query.filter(Report.user_id == user_id)
            else:
                query = query.filter(Report.user_id.is_(None))
            report = query.first()

            if report:
                report.diet_plan = diet_plan
    except DatabaseError as error:
        raise _raise_operation_error("update the diet plan", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("update the diet plan", error) from error


def save_message(report_id: int, role: str, content: str, user_id: int | None = None):
    try:
        with get_session() as session:
            if not _verify_report_ownership(session, report_id, user_id):
                raise PermissionError("Report does not belong to the user")
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


def get_chat_history(report_id: int, user_id: int | None = None):
    try:
        with get_session() as session:
            if not _verify_report_ownership(session, report_id, user_id):
                return []
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


def get_all_reports(user_id: int | None = None):
    try:
        with get_session() as session:
            query = session.query(Report)
            if user_id is not None:
                query = query.filter(Report.user_id == user_id)
            else:
                query = query.filter(Report.user_id.is_(None))
            
            reports = query.order_by(Report.created_at.desc()).all()

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


def get_report_by_id(report_id: int, user_id: int | None = None):
    try:
        with get_session() as session:
            query = session.query(Report).filter(Report.id == report_id)
            if user_id is not None:
                query = query.filter(Report.user_id == user_id)
            else:
                query = query.filter(Report.user_id.is_(None))
            report = query.first()

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


def delete_report(report_id: int, user_id: int | None = None):
    try:
        with get_session() as session:
            query = session.query(Report).filter(Report.id == report_id)
            if user_id is not None:
                query = query.filter(Report.user_id == user_id)
            else:
                query = query.filter(Report.user_id.is_(None))
            report = query.first()

            if report:
                session.delete(report)
    except DatabaseError as error:
        raise _raise_operation_error("delete the report", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("delete the report", error) from error
    
def get_dashboard_stats(user_id: int | None = None):
    try:
        with get_session() as session:

            query = session.query(Report)

            if user_id is not None:
                query = query.filter(Report.user_id == user_id)
            else:
                query = query.filter(Report.user_id.is_(None))

            reports = query.order_by(Report.created_at.desc()).all()

            total_reports = len(reports)

            if total_reports == 0:
                return {
                    "health_score": "--",
                    "reports": 0,
                    "risk": "--",
                    "ai_status": "Ready"
                }

            latest = reports[0]

            extracted = latest.extracted_values or ""

            high_count = extracted.upper().count("STATUS: HIGH")
            low_count = extracted.upper().count("STATUS: LOW")

            if high_count >= 5:
                risk = "High"
            elif high_count >= 2:
                risk = "Medium"
            else:
                risk = "Low"

            total_tests = (
                extracted.upper().count("STATUS:")
                if extracted else 0
            )

            if total_tests == 0:
                health_score = "--"
            else:
                abnormal = high_count + low_count
                score = max(0, 100 - abnormal * 8)
                health_score = str(score)

            return {
                "health_score": health_score,
                "reports": total_reports,
                "risk": risk,
                "ai_status": "Ready"
            }

    except DatabaseError as error:
        raise _raise_operation_error("load dashboard statistics", error) from error
    except SQLAlchemyError as error:
        raise _raise_operation_error("load dashboard statistics", error) from error
    
def get_dashboard_stats(user_id: int | None = None):
    try:
        with get_session() as session:

            query = session.query(Report)

            if user_id is not None:
                query = query.filter(Report.user_id == user_id)
            else:
                query = query.filter(Report.user_id.is_(None))

            reports = query.order_by(Report.created_at.desc()).all()

            total_reports = len(reports)

            latest = reports[0] if reports else None

            health_score = "--"
            risk = "--"

            if latest and latest.extracted_values:

                extracted = latest.extracted_values.upper()

                high = extracted.count("STATUS: HIGH")
                low = extracted.count("STATUS: LOW")
                abnormal = high + low
                total = extracted.count("STATUS:")

                if total > 0:
                    score = max(0, 100 - abnormal * 8)
                    health_score = str(score)

                if high >= 5:
                    risk = "High"
                elif high >= 2:
                    risk = "Medium"
                else:
                    risk = "Low"

            return {
                "health_score": health_score,
                "reports": total_reports,
                "risk": risk,
                "status": "Online",
            }

    except DatabaseError as error:
        raise _raise_operation_error("load dashboard statistics", error) from error

    except SQLAlchemyError as error:
        raise _raise_operation_error("load dashboard statistics", error) from error