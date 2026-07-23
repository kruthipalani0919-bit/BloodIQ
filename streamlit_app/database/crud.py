from sqlalchemy.exc import SQLAlchemyError

from database.connection import (
    get_session,
    initialize_database,
    supabase,
)

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


def save_report(report_text: str, user_id: int | None = None) -> int:
    try:
        data = {
            "report_text": report_text,
            "user_id": user_id,
        }

        response = (
            supabase.table("reports")
            .insert(data)
            .execute()
        )

        print(response)

        return response.data[0]["id"]

    except Exception as error:
        print("SUPABASE ERROR:", error)
        raise

def update_analysis(report_id: int, extracted_values: str, user_id: int | None = None):
    try:
        (
            supabase.table("reports")
            .update(
                {
                    "extracted_values": extracted_values
                }
            )
            .eq("id", report_id)
            .execute()
        )

    except Exception as error:
        raise _raise_operation_error("update the analysis", error) from error

def update_diet(report_id: int, diet_plan: str, user_id: int | None = None):
    try:
        (
            supabase.table("reports")
            .update(
                {
                    "diet_plan": diet_plan
                }
            )
            .eq("id", report_id)
            .execute()
        )

    except Exception as error:
        raise _raise_operation_error("update the diet plan", error) from error

def save_message(report_id: int, role: str, content: str, user_id: int | None = None):
    try:
        data = {
            "report_id": report_id,
            "role": role,
            "content": content,
        }

        supabase.table("chat_messages").insert(data).execute()

    except Exception as error:
        raise _raise_operation_error("save the chat message", error) from error

def get_chat_history(report_id: int, user_id: int | None = None):
    try:
        response = (
            supabase.table("chat_messages")
            .select("*")
            .eq("report_id", report_id)
            .order("created_at")
            .execute()
        )

        return [
            {
                "role": msg["role"],
                "content": msg["content"],
            }
            for msg in response.data
        ]

    except Exception as error:
        raise _raise_operation_error("load the chat history", error) from error

def get_all_reports(user_id: int | None = None):
    try:
        query = (
            supabase.table("reports")
            .select("*")
            .order("created_at", desc=True)
        )

        if user_id is not None:
            query = query.eq("user_id", user_id)

        response = query.execute()

        reports = response.data

        return [
            {
                "id": report["id"],
                "created_at": report["created_at"],
                "preview": (
                    report["report_text"][:60].replace("\n", " ") + "..."
                )
                if report.get("report_text")
                else "...",
                "has_diet": report.get("diet_plan") is not None,
                "has_analysis": report.get("extracted_values") is not None,
            }
            for report in reports
        ]

    except Exception as error:
        raise _raise_operation_error("load reports", error) from error

def get_report_by_id(report_id: int, user_id: int | None = None):
    try:
        query = (
            supabase.table("reports")
            .select("*")
            .eq("id", report_id)
        )

        if user_id is not None:
            query = query.eq("user_id", user_id)

        response = query.execute()

        if not response.data:
            return None

        report = response.data[0]

        return {
            "id": report["id"],
            "report_text": report.get("report_text"),
            "extracted_values": report.get("extracted_values"),
            "diet_plan": report.get("diet_plan"),
        }

    except Exception as error:
        raise _raise_operation_error("load the report", error) from error

def delete_report(report_id: int, user_id: int | None = None):
    try:
        (
            supabase.table("reports")
            .delete()
            .eq("id", report_id)
            .execute()
        )

    except Exception as error:
        raise _raise_operation_error("delete the report", error) from error
        raise _raise_operation_error("delete the report", error) from error
def get_dashboard_stats(user_id: int | None = None):
    try:
        query = (
            supabase.table("reports")
            .select("*")
            .order("created_at", desc=True)
        )

        if user_id is not None:
            query = query.eq("user_id", user_id)

        response = query.execute()
        reports = response.data

        total_reports = len(reports)

        if total_reports == 0:
            return {
                "health_score": "--",
                "reports": 0,
                "risk": "--",
                "status": "Online",
            }

        latest = reports[0]
        extracted = (latest.get("extracted_values") or "").upper()

        high = extracted.count("STATUS: HIGH")
        low = extracted.count("STATUS: LOW")
        abnormal = high + low
        total = extracted.count("STATUS:")

        health_score = "--"
        if total > 0:
            health_score = str(max(0, 100 - abnormal * 8))

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

    except Exception as error:
        raise _raise_operation_error("load dashboard statistics", error) from error