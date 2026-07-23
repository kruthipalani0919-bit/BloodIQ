# """Verification script for BloodIQ platform foundation."""
# import sys
# import os

# # Ensure the streamlit_app directory is on the path
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# from database.connection import get_session, initialize_database, verify_database_connection
# from database.crud import save_report, get_all_reports, get_report_by_id, delete_report
# from services.auth_service import register_user, authenticate_user, verify_token, get_user_by_email


# def run_tests():
#     print("1. Testing DB connection...")
#     verify_database_connection()
#     print("   OK")

#     print("2. Initializing Database (auto-migrations)...")
#     initialize_database()
#     print("   OK")

#     with get_session() as db:
#         test_email = "platform_test_runner@bloodiq.dev"
#         existing = get_user_by_email(db, test_email)
#         if existing:
#             db.delete(existing)
#             db.flush()

#         print("3. Registering test user...")
#         user = register_user(db, test_email, "TestPass!99", "Test Runner", age=28, gender="Male")
#         db.flush()
#         assert user.id is not None, "User ID should be set after flush"
#         print(f"   Registered user ID={user.id}")

#         print("4. Authenticating test user...")
#         result = authenticate_user(db, test_email, "TestPass!99")
#         assert result is not None, "Authentication should succeed"
#         auth_user, token = result
#         assert auth_user.id == user.id
#         print(f"   Token: {token[:30]}...")

#         print("5. Verifying JWT token...")
#         uid = verify_token(token)
#         assert uid == user.id, f"Token decoded user_id={uid}, expected {user.id}"
#         print("   OK")

#         print("6. Wrong password should fail...")
#         bad = authenticate_user(db, test_email, "WrongPassword")
#         assert bad is None, "Wrong password should return None"
#         print("   OK")

#     # Test user-scoped CRUD
#     with get_session() as db:
#         user = get_user_by_email(db, test_email)
#         uid = user.id

#         print("7. Saving user-scoped report...")
#         rid = save_report("Hemoglobin: 14.5 g/dL", user_id=uid)
#         print(f"   Report ID={rid}")

#         print("8. Saving guest report...")
#         gid = save_report("Hemoglobin: 10.0 g/dL", user_id=None)
#         print(f"   Guest Report ID={gid}")

#     with get_session() as db:
#         print("9. User report listing isolation...")
#         user_reports = get_all_reports(user_id=uid)
#         guest_reports = get_all_reports(user_id=None)
#         user_ids = {r["id"] for r in user_reports}
#         guest_ids = {r["id"] for r in guest_reports}
#         assert rid in user_ids, "User report missing from user listing"
#         assert rid not in guest_ids, "User report leaked to guest listing"
#         assert gid in guest_ids, "Guest report missing from guest listing"
#         assert gid not in user_ids, "Guest report leaked to user listing"
#         print("   OK")

#         print("10. Report-by-ID ownership check...")
#         assert get_report_by_id(rid, user_id=uid) is not None
#         assert get_report_by_id(rid, user_id=None) is None
#         assert get_report_by_id(gid, user_id=None) is not None
#         assert get_report_by_id(gid, user_id=uid) is None
#         print("   OK")

#     # Cleanup
#     with get_session() as db:
#         print("11. Cleanup...")
#         delete_report(rid, user_id=uid)
#         delete_report(gid, user_id=None)

#     with get_session() as db:
#         user = get_user_by_email(db, test_email)
#         if user:
#             db.delete(user)
#         print("   OK")

#     print("\n=== ALL PLATFORM FOUNDATION TESTS PASSED ===")


# if __name__ == "__main__":
#     run_tests()
