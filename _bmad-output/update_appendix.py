with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'r', encoding='utf-8') as f:
    content = f.read()

old_appendix = """## 11. Appendix: Assignment Checklist (from PPTX + Your Requirements)

| PPTX/口頭要求 | Covered In |
|------------------|------------|
| MVVM / MVC architecture awareness | Section 5 (architecture diagram + MVC mapping) |
| CRUD ↔ SQL ↔ HTTP mapping | Section 3.2 (API spec with SQL ↔ HTTP mapping) |
| PostgreSQL (pgSQL) database | Section 3.1, Phase 1 |
| Flask backend | Section 5, Phase 2 |
| **Flask-Migrate 資料庫遷移** | Phase 1 (flask db init/migrate/upgrade) |
| dbdiagram.io ER diagram | Phase 1, US-5.1 |
| AI + Database (AILearn) | `AIlearn` DB created ✅ |
| Markdown schema export | US-5.3, Phase 1 |
| **前端 React + TypeScript** | Phase 3 (Vite + React + TS + Tailwind) |
| **隨時知道那些品項需要補貨** | US-3.1, US-3.2, US-3.3, Phase 3 (補貨提醒 tab) |
| **查看每個銷貨員的業績** | US-4.1~US-4.4, Section 3.1 (salesperson table), Section 3.2 (reports API), Phase 3 (業績報表 tab) |
| **課程教學用途** | Section 4 (Educational Value), Phase 4 (Documentation) |"""

new_appendix = """## 11. Appendix: Assignment Checklist (from PPTX + Your Requirements + Research Enhancements)

| PPTX/口頭要求 / 研究增強 | Covered In |
|------------------|------------|
| MVVM / MVC architecture awareness | Section 5 (architecture diagram + MVC mapping) |
| CRUD ↔ SQL ↔ HTTP mapping | Section 3.2 (API spec with SQL ↔ HTTP mapping) |
| PostgreSQL (pgSQL) database | Section 3.1, Phase 1 |
| Flask backend | Section 5, Phase 2 |
| **Flask-Migrate 資料庫遷移** | Phase 1 (flask db init/migrate/upgrade) |
| dbdiagram.io ER diagram | Phase 1, US-5.1 |
| AI + Database (AILearn) | `AIlearn` DB created ✅ |
| Markdown schema export | US-5.3, Phase 1 |
| **前端 React + TypeScript** | Phase 3 (Vite + React + TS + Tailwind) |
| **隨時知道那些品項需要補貨** | US-3.1, US-3.2, US-3.3, Phase 3 (補貨提醒 tab + PO 生成) |
| **查看每個銷貨員的業績** | US-4.1~US-4.4, Section 3.1 (salesperson table), Section 3.2 (reports API), Phase 3 (業績報表 tab + Leaderboard) |
| **課程教學用途** | Section 4 (Educational Value), Phase 4 (Documentation + Seed Data + Tests) |
| **分層分類** | InvenTree 參考 → Category.parent_id + path |
| **供應商管理** | InvenTree 參考 → Supplier + ProductSupplier (supplier_sku, price) |
| **多倉位庫存** | InvenTree 參考 → Location + StockItem (per-location qty) |
| **價格快照** | flask-react-inventory 參考 → StockMovement.unit_price_at_time |
| **僅追加流水帳** | flask-react-inventory 參考 → StockMovement ON DELETE RESTRICT |
| **保留/可用庫存** | flask-react-inventory 參考 → reserved_stock / available_stock |
| **角色權限** | flask-react-inventory 參考 → Admin/Manager/Staff 視圖差異 |
| **價格歷史報表** | flask-react-inventory 參考 → unit_price_at_time 用於毛利計算 |
| **供應商分組採購單** | InvenTree 參考 → Reorder suggestions grouped by supplier |
| **React Query 快取** | flask-react-inventory 參考 → TanStack Query staleTime/invalidate |
| **Vite Proxy 無 CORS** | flask-react-inventory 參考 → /api -> Flask 5000 |
| **種子資料 CLI** | flask-react-inventory 參考 → `flask seed-demo` |
| **測試資料庫隔離** | flask-react-inventory 參考 → `_test` 後綴獨立 DB |
| **Pre-commit 品質** | Best practice → ruff + eslint + pre-commit hooks |"""

if old_appendix in content:
    content = content.replace(old_appendix, new_appendix)
    print("Appendix updated!")
else:
    print("Appendix NOT FOUND")

with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'w', encoding='utf-8') as f:
    f.write(content)