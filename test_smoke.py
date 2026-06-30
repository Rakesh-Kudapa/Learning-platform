"""
Smoke tests — verifies that key pages load, module 3 is wired, and /api/ask works.
Run:  python test_smoke.py
"""
import sys, os, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db, User
from course_data import MODULE_CONTEXT, MODULE_TITLES, TEST_QUESTIONS, PASS_MARK

def smoke():
    app = create_app()
    app.config["TESTING"] = True

    ok, fail = 0, 0

    def check(name, cond):
        nonlocal ok, fail
        if cond:
            ok += 1
            print(f"  PASS  {name}")
        else:
            fail += 1
            print(f"  FAIL  {name}")

    with app.test_client() as c:
        r = c.get("/health")
        check("GET /health returns 200", r.status_code == 200)

        r = c.get("/course")
        check("GET /course redirects when not logged in", r.status_code in (302, 301))

        email = f"smoke{int(time.time()*1000)}@test.local"
        r = c.post("/register", data={"name": "SmokeTest", "email": email, "password": "test1234"}, follow_redirects=True)
        check("POST /register succeeds", r.status_code == 200)

        r = c.get("/course")
        check("GET /course returns 200 after login", r.status_code == 200)

        html = r.data.decode()
        check("course.html contains mod3 function", "function mod3()" in html)
        check("course.html contains MODULE 03 eyebrow", "MODULE 03" in html)
        check("course.html contains pipeline SVG function", "function pipelineSVG()" in html)
        check("COURSE[] has module 3 as content type", "type:'content',body:mod3" in html)
        check("Module 3 knowledge check wired", "Which step comes right after data is standardized" in html)
        check("COURSE[] uses checks array format", "checks:[{" in html)
        check("checkBlock renders multi-question", "function checkBlock" in html and "allChecked" in html)
        check("answer() takes qIdx parameter", "answer(i,qi,j)" in html)
        check("Module 3 narration text present", "Real-world data starts out messy" in html)

        check("course.html contains doubtPanel function", "function doubtPanel(" in html)
        check("course.html contains askDoubt function", "function askDoubt(" in html)
        check("doubt panel wired into mod1", "doubtPanel(0)" in html)
        check("doubt panel wired into mod2", "doubtPanel(1)" in html)
        check("doubt panel wired into mod3", "doubtPanel(2)" in html)

        r = c.post("/api/ask", json={}, content_type="application/json")
        check("POST /api/ask rejects missing module_id", r.status_code == 400)

        r = c.post("/api/ask", json={"module_id": 0}, content_type="application/json")
        check("POST /api/ask rejects missing question", r.status_code == 400)

        r = c.post("/api/ask", json={"module_id": 99, "question": "test"}, content_type="application/json")
        check("POST /api/ask rejects invalid module_id", r.status_code == 400)

        # --- Modules 4-12 wiring ---
        for n, fn in [(4,"mod4"),(5,"mod5"),(6,"mod6"),(7,"mod7"),(8,"mod8"),
                      (9,"mod9"),(10,"mod10"),(11,"mod11"),(12,"mod12")]:
            check(f"course.html contains {fn}()", f"function {fn}()" in html)
        check("COURSE[] no longer has any locked modules", "type:'locked'" not in html)
        check("Module 4 flashcard grid wired", "flash-grid" in html)
        check("Module 12 References has no checks (reference-only)", "body:mod12}" in html)
        check("doubt panel wired into all 12 modules", all(f"doubtPanel({i})" in html for i in range(12)))

        # --- Final exam endpoints ---
        r = c.get("/api/test")
        check("GET /api/test returns 200", r.status_code == 200)
        questions = r.get_json()
        check("GET /api/test returns all questions", len(questions) == len(TEST_QUESTIONS))
        check("GET /api/test never exposes the answer key", all("answer" not in q for q in questions))

        correct_answers = {str(i): q["answer"] for i, q in enumerate(TEST_QUESTIONS)}
        r = c.post("/api/test/submit", json={"answers": correct_answers}, content_type="application/json")
        result = r.get_json()
        check("POST /api/test/submit scores a perfect run as passed", result["passed"] is True and result["score"] == len(TEST_QUESTIONS))

        wrong_answers = {str(i): (q["answer"] + 1) % len(q["options"]) for i, q in enumerate(TEST_QUESTIONS)}
        r = c.post("/api/test/submit", json={"answers": wrong_answers}, content_type="application/json")
        check("POST /api/test/submit scores an all-wrong run as failed", r.get_json()["passed"] is False)

        r = c.get("/api/test/results")
        results = r.get_json()
        check("GET /api/test/results returns best attempt", results["best"]["score"] == len(TEST_QUESTIONS))
        check("GET /api/test/results reports correct pass_mark", results["pass_mark"] == PASS_MARK)

    # --- Admin dashboard tests ---
    os.environ["ADMIN_EMAIL"] = email  # the smoke user is now admin
    app2 = create_app()
    app2.config["TESTING"] = True
    with app2.test_client() as c2:
        c2.post("/login", data={"email": email, "password": "test1234"}, follow_redirects=True)

        r = c2.get("/admin")
        check("GET /admin returns 200 for admin user", r.status_code == 200)
        check("admin.html contains Chart.js", b"chart.js" in r.data.lower() or b"Chart" in r.data)

        r = c2.get("/api/admin/stats")
        check("GET /api/admin/stats returns 200", r.status_code == 200)
        import json as _json
        stats = _json.loads(r.data)
        check("stats has total_users key", "total_users" in stats)
        check("stats has users list", isinstance(stats.get("users"), list))
        check("stats has registrations_by_date", "registrations_by_date" in stats)
        check("stats has pre_knowledge", "pre_knowledge" in stats)
        check("stats has doubts_per_module", "doubts_per_module" in stats)
        check("stats has test_pass_fail", "test_pass_fail" in stats)

        r = c2.get("/api/admin/answer-key")
        check("GET /api/admin/answer-key returns 200", r.status_code == 200)
        key = r.get_json()
        check("answer-key has modules list", isinstance(key.get("modules"), list) and len(key["modules"]) == 12)
        check("answer-key modules carry full answer+explain", all(
            ("answer" in qq and "explain" in qq) for m in key["modules"] for qq in m["questions"]
        ))
        check("answer-key Module 12 (References) has zero questions", key["modules"][11]["questions"] == [])
        check("answer-key has final_exam with answers exposed (admin-only)", all("answer" in q for q in key["final_exam"]))
        check("answer-key final_exam matches TEST_QUESTIONS length", len(key["final_exam"]) == len(TEST_QUESTIONS))

        r = c2.get("/api/me")
        check("GET /api/me reports is_admin true for the admin account", r.get_json().get("is_admin") is True)

        r = c2.get("/course")
        check("Admin can still access /course (universal access)", r.status_code == 200)

    # Verify non-admin can't access admin routes or the answer key
    with app2.test_client() as c3:
        other_email = f"other{int(time.time()*1000)}@test.local"
        c3.post("/register", data={"name": "Other", "email": other_email, "password": "test1234"}, follow_redirects=True)
        r = c3.get("/admin", follow_redirects=False)
        check("GET /admin redirects non-admin user", r.status_code == 302)
        r = c3.get("/api/admin/answer-key", follow_redirects=False)
        check("GET /api/admin/answer-key redirects non-admin user", r.status_code == 302)
        r = c3.get("/api/me")
        check("GET /api/me reports is_admin false for a regular user", r.get_json().get("is_admin") is False)

    # --- Multi-admin grant/revoke + per-user module unlock overrides ---
    with app2.app_context():
        other_user = User.query.filter_by(email=other_email).first()
        other_user_id = other_user.id

    with app2.test_client() as c2b:
        c2b.post("/login", data={"email": email, "password": "test1234"}, follow_redirects=True)

        r = c2b.post("/api/admin/unlock", json={"user_id": other_user_id, "module_id": 5}, content_type="application/json")
        check("POST /api/admin/unlock succeeds", r.status_code == 200)
        r = c2b.get("/api/admin/stats")
        target = next(u for u in r.get_json()["users"] if u["id"] == other_user_id)
        check("Unlocked module appears in stats for that user", target["unlocked_modules"] == [5])

        r = c2b.post("/api/admin/lock", json={"user_id": other_user_id, "module_id": 5}, content_type="application/json")
        check("POST /api/admin/lock succeeds", r.status_code == 200)
        r = c2b.get("/api/admin/stats")
        target = next(u for u in r.get_json()["users"] if u["id"] == other_user_id)
        check("Locked module removed from unlocked list", target["unlocked_modules"] == [])

        r = c2b.post("/api/admin/unlock-all", json={"user_id": other_user_id}, content_type="application/json")
        r = c2b.get("/api/admin/stats")
        target = next(u for u in r.get_json()["users"] if u["id"] == other_user_id)
        check("unlock-all unlocks every module", sorted(target["unlocked_modules"]) == list(range(12)))

        r = c2b.post("/api/admin/lock-all", json={"user_id": other_user_id}, content_type="application/json")
        r = c2b.get("/api/admin/stats")
        target = next(u for u in r.get_json()["users"] if u["id"] == other_user_id)
        check("lock-all clears every module", target["unlocked_modules"] == [])

        r = c2b.post("/api/admin/unlock", json={"user_id": other_user_id, "module_id": 99}, content_type="application/json")
        check("POST /api/admin/unlock rejects invalid module_id", r.status_code == 400)

        # Grant admin access to the other user (super admin only)
        r = c2b.get("/api/admin/admins")
        admins = r.get_json()
        check("GET /api/admin/admins reports primary admin", admins["super_admin"] == email)
        check("Current session is recognized as super admin", admins["is_super_admin"] is True)

        r = c2b.post("/api/admin/admins", json={"email": other_email}, content_type="application/json")
        check("POST /api/admin/admins grants access", r.status_code == 200)

        r = c2b.get("/api/admin/admins")
        check("Granted admin now appears in admins list", any(g["email"] == other_email for g in r.get_json()["granted"]))

    # The newly-granted admin should now have admin access, but NOT be able to grant further admins
    with app2.test_client() as c5:
        c5.post("/login", data={"email": other_email, "password": "test1234"}, follow_redirects=True)
        r = c5.get("/api/me")
        check("Granted admin's /api/me now reports is_admin true", r.get_json().get("is_admin") is True)
        r = c5.get("/admin")
        check("Granted admin can reach /admin", r.status_code == 200)
        r = c5.post("/api/admin/admins", json={"email": "someoneelse@test.local"}, content_type="application/json")
        check("Granted (non-super) admin cannot grant further admins", r.status_code == 403)

    # Revoke the granted admin's access (super admin only)
    with app2.test_client() as c2c:
        c2c.post("/login", data={"email": email, "password": "test1234"}, follow_redirects=True)
        r = c2c.post("/api/admin/admins/revoke", json={"email": email}, content_type="application/json")
        check("Primary admin cannot be revoked from the portal", r.status_code == 400)

        r = c2c.post("/api/admin/admins/revoke", json={"email": other_email}, content_type="application/json")
        check("POST /api/admin/admins/revoke revokes access", r.status_code == 200)

    with app2.test_client() as c6:
        c6.post("/login", data={"email": other_email, "password": "test1234"}, follow_redirects=True)
        r = c6.get("/api/me")
        check("Revoked user's is_admin is false again", r.get_json().get("is_admin") is False)
        r = c6.get("/admin", follow_redirects=False)
        check("Revoked user can no longer reach /admin", r.status_code == 302)

        # Sync some progress for this learner, then verify admin can read it back
        r = c6.post("/api/progress", json={"xp": 60, "done": {"0": True}, "checks": {"0": [True]}, "badges": ["first"], "current": 1}, content_type="application/json")
        check("POST /api/progress saves successfully", r.status_code == 200)
        r = c6.post("/api/feedback", json={"rating": 4, "experience": "Good course", "suggestions": "More videos"}, content_type="application/json")
        check("POST /api/feedback for report test", r.status_code == 200)
        r = c6.post("/api/contributions", json={"title": "Tip", "content": "Use OMOP early"}, content_type="application/json")
        check("POST /api/contributions for report test", r.status_code == 200)

    # --- Per-user admin actions: performance report, edit, delete ---
    with app2.test_client() as c2d:
        c2d.post("/login", data={"email": email, "password": "test1234"}, follow_redirects=True)

        r = c2d.get(f"/api/admin/users/{other_user_id}/report")
        check("GET /api/admin/users/<id>/report returns 200", r.status_code == 200)
        report = r.get_json()
        check("Report includes synced module progress", report["progress"]["xp"] == 60)
        check("Report module 1 shows 1/1 correct", report["progress"]["modules"][0]["correct"] == 1)
        check("Report includes feedback", len(report["feedback"]) == 1 and report["feedback"][0]["rating"] == 4)
        check("Report includes contributions", len(report["contributions"]) == 1)

        new_email = f"renamed{int(time.time()*1000)}@test.local"
        r = c2d.patch(f"/api/admin/users/{other_user_id}", json={"name": "Renamed User", "email": new_email}, content_type="application/json")
        check("PATCH /api/admin/users/<id> edits name/email", r.status_code == 200)
        r = c2d.get("/api/admin/stats")
        edited = next(u for u in r.get_json()["users"] if u["id"] == other_user_id)
        check("Edited user shows new name", edited["name"] == "Renamed User")
        check("Edited user shows new email", edited["email"] == new_email)

        r = c2d.delete(f"/api/admin/users/{other_user_id}")
        check("DELETE /api/admin/users/<id> removes the user", r.status_code == 200)
        r = c2d.get("/api/admin/stats")
        check("Deleted user no longer appears in stats", not any(u["id"] == other_user_id for u in r.get_json()["users"]))

        # Safety checks: can't delete primary admin or self
        with app2.app_context():
            admin_user = User.query.filter_by(email=email).first()
        r = c2d.delete(f"/api/admin/users/{admin_user.id}")
        check("Primary admin account can't be deleted", r.status_code == 400)

    # --- Bulk delete ---
    with app2.test_client() as c2e:
        c2e.post("/login", data={"email": email, "password": "test1234"}, follow_redirects=True)
        bulk_emails = [f"bulk{i}_{int(time.time()*1000)}@test.local" for i in range(2)]
        bulk_ids = []
        for be in bulk_emails:
            c2e.post("/register", data={"name": "Bulk", "email": be, "password": "test1234"})
            c2e.get("/logout")
            c2e.post("/login", data={"email": email, "password": "test1234"}, follow_redirects=True)
        with app2.app_context():
            bulk_ids = [User.query.filter_by(email=be).first().id for be in bulk_emails]
        r = c2e.post("/api/admin/users/bulk-delete", json={"user_ids": bulk_ids}, content_type="application/json")
        check("POST /api/admin/users/bulk-delete succeeds", r.status_code == 200 and r.get_json()["deleted"] == 2)
        r = c2e.get("/api/admin/stats")
        remaining_ids = [u["id"] for u in r.get_json()["users"]]
        check("Bulk-deleted users are gone from stats", not any(bid in remaining_ids for bid in bulk_ids))

    # Verify admin has full access even when APP_MODE=user (universal access)
    os.environ["APP_MODE"] = "user"
    app3 = create_app()
    app3.config["TESTING"] = True
    with app3.test_client() as c4:
        c4.post("/login", data={"email": email, "password": "test1234"}, follow_redirects=True)
        r = c4.get("/admin", follow_redirects=False)
        check("Admin reaches /admin even when APP_MODE=user", r.status_code == 200)
    del os.environ["APP_MODE"]

    check("MODULE_TITLES has 12 entries", len(MODULE_TITLES) == 12)
    check("MODULE_TITLES[2] is End-to-End Process", MODULE_TITLES[2] == "End-to-End Process")
    check("MODULE_CONTEXT has key 2", 2 in MODULE_CONTEXT)
    check("MODULE_CONTEXT[2] mentions six stages", "six stages" in MODULE_CONTEXT[2])
    check("PASS_MARK is 75%", PASS_MARK == 0.75)
    check("TEST_QUESTIONS covers all 11 content modules", len(TEST_QUESTIONS) == 13)

    print(f"\n{'='*40}")
    print(f"  {ok} passed, {fail} failed")
    if fail:
        print("  SOME TESTS FAILED")
        sys.exit(1)
    else:
        print("  ALL SMOKE TESTS PASSED")

if __name__ == "__main__":
    smoke()
