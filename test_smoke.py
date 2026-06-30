"""
Smoke tests — verifies that key pages load, module 3 is wired, and /api/ask works.
Run:  python test_smoke.py
"""
import sys, os, time
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from models import db
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
