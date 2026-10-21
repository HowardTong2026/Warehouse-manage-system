with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'r', encoding='utf-8') as f:
    content = f.read()

old_risks = """## 9. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| PostgreSQL connection issues | Medium | High | Use `.env` with verified credentials; test `pg_isready` first |
| Stock race condition | Low | High | Use single transaction: `UPDATE product SET current_stock = current_stock + :qty WHERE id = :id RETURNING current_stock` + INSERT movement |
| SKU collision on concurrent create | Low | Medium | DB unique constraint + catch IntegrityError → 409 response |
| Salesperson FK violation on stock_out | Medium | High | Frontend: disable submit until salesperson selected; Backend: validate FK |
| Report query performance | Low | Medium | Proper indexes (idx_stock_movement_salesperson, idx_stock_movement_type_created); date range filtering |
| Time constraints | High | Medium | Scope to MVP (Must-haves only); defer Could (CSV export) |"""

new_risks = """## 9. Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| PostgreSQL connection issues | Medium | High | Use `.env` with verified credentials; test `pg_isready` first; separate test DB (`_test` suffix) |
| Stock race condition | Low | High | Single transaction: `UPDATE ... RETURNING` + INSERT movement; `SELECT FOR UPDATE` if needed |
| SKU/barcode collision | Low | Medium | DB unique constraints + catch `IntegrityError` → 409 with field details |
| Salesperson FK violation on stock_out | Medium | High | Frontend: disable submit until valid salesperson; Backend: validate active FK |
| Report query performance | Low | Medium | Composite indexes (salesperson+created, type+created); date range partitioning ready |
| Time constraints | High | Medium | MVP scope (Must-haves); defer Could (CSV export, batch/serial tracking, multi-location UI) |
| Migration conflicts | Low | High | Review generated migrations; never edit applied migrations; use `flask db revision` for manual |
| Vite proxy CORS in dev | Medium | Medium | Configure `server.proxy` in `vite.config.ts`; `/api` → `http://localhost:5000` |
| TanStack Query stale data | Low | Medium | `staleTime: 30s`; `invalidateQueries` on mutations; optimistic updates for stock |
| Hierarchical tree performance | Low | Low | Materialized `path` column; lazy-load children; virtualized list for 1000+ nodes |"""

if old_risks in content:
    content = content.replace(old_risks, new_risks)
    print("Risks updated!")
else:
    print("Risks NOT FOUND")

with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'w', encoding='utf-8') as f:
    f.write(content)