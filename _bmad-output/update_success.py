with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'r', encoding='utf-8') as f:
    content = f.read()

old_success = """## 10. Success Criteria

1. **Functional:** All Must-have user stories pass manual testing
2. **Database:** `flask db upgrade` creates schema cleanly on fresh `AIlearn` DB; migrations are version-controlled
3. **API:** All 15 endpoints respond correctly with JSON; validated via marshmallow schemas
4. **Frontend:** React app with 4 tabs loads, performs all operations; TypeScript compiles without errors
5. **Documentation:** `schema.md`, `README.md`, dbdiagram.io link present; migration history in `migrations/versions/`
6. **Assignment Alignment:** Matches PPTX requirements (MVVM/MVC awareness, CRUD↔SQL↔HTTP, PostgreSQL, Flask, dbdiagram.io)
7. **Educational Quality:** Code is readable, commented, modular — suitable as teaching reference; demonstrates React + Flask + Flask-Migrate best practices"""

new_success = """## 10. Success Criteria

1. **Functional:** All Must-have user stories pass manual testing (CRUD + stock in/out/transfer + alerts + salesperson + reports)
2. **Database:** `flask db upgrade` creates schema cleanly on fresh `AIlearn` DB; migrations version-controlled in `migrations/versions/`
3. **API:** All 20+ endpoints respond correctly with JSON; validated via marshmallow schemas; consistent error format
4. **Frontend:** React app with 5 tabs + dashboard loads, performs all operations; TypeScript compiles without errors; TanStack Query caching works
5. **Documentation:** `schema.md` (Chinese), `README.md` (full setup), dbdiagram.io link; migration history in `migrations/versions/`
6. **Assignment Alignment:** Matches PPTX requirements (MVVM/MVC awareness, CRUD↔SQL↔HTTP, PostgreSQL, Flask, dbdiagram.io, React, Flask-Migrate)
7. **Educational Quality:** Code readable, commented, modular — suitable as teaching reference; demonstrates React + Flask + Flask-Migrate + TanStack Query best practices
8. **Testing:** `pytest` passes (unit + integration); `npm test` passes; test DB separate; CI-ready
9. **DevEx:** `flask seed-demo` works; `npm run dev` + `flask run` hot reload; `flask db` CLI functional; pre-commit hooks configured"""

if old_success in content:
    content = content.replace(old_success, new_success)
    print("Success criteria updated!")
else:
    print("Success criteria NOT FOUND")

with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'w', encoding='utf-8') as f:
    f.write(content)