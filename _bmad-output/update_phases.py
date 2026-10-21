with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'r', encoding='utf-8') as f:
    content = f.read()

old_phases = """## 8. Implementation Phases

### Phase 1: Backend Setup + Database Migrations (Day 1)
- [ ] Create Python virtualenv: `python -m venv venv && source venv/bin/activate`
- [ ] Install deps: `pip install flask flask-sqlalchemy flask-migrate psycopg2-binary python-dotenv marshmallow`
- [ ] Create `config.py` with `SQLALCHEMY_DATABASE_URI` from `.env`
- [ ] Create `models/` with SQLAlchemy models (Category, Product, Salesperson, StockMovement)
- [ ] Create `app.py` with Flask app factory + `db.init_app(app)` + `Migrate(app, db)`
- [ ] Run `flask db init` → `flask db migrate -m "initial schema"` → `flask db upgrade`
- [ ] Verify tables in pgAdmin (AIlearn database)
- [ ] Export ER diagram from pgAdmin or dbdiagram.io → `schema.md`

### Phase 2: Backend API + Services (Day 1-2)
- [ ] Implement `services/` (business logic: transactions, validation, aggregations)
- [ ] Implement `schemas/` (request/response validation with marshmallow)
- [ ] Implement `routes/` (Blueprints: products, stock, alerts, salespeople, reports)
- [ ] Register blueprints in `app.py` with `/api` prefix
- [ ] Test all 15 endpoints with curl/Postman — verify transactions, FK constraints, report queries

### Phase 3: React Frontend (Day 2)
- [ ] Initialize: `cd frontend && npm create vite@latest . -- --template react-ts`
- [ ] Install: `npm install && npm install axios tailwindcss @tailwindcss/vite && npx tailwindcss init`
- [ ] Configure Vite proxy to Flask (`/api` → `http://localhost:5000`)
- [ ] Build `api/client.ts` (Axios instance) + `api/endpoints.ts`
- [ ] Create custom hooks: `useProducts`, `useStock`, `useSalespeople`, `useReports`
- [ ] Build 4 page components: `ProductsPage`, `StockPage`, `AlertsPage`, `ReportsPage`
- [ ] Shared UI components: `DataTable`, `Modal`, `Form`, `KPICard`, `Chart`
- [ ] Style with Tailwind CSS (responsive, accessible)

### Phase 4: Integration + Polish + Documentation (Day 2-3)
- [ ] End-to-end testing (CRUD + stock in/out + alerts + salesperson + reports)
- [ ] Verify Flask-Migrate works: `flask db migrate -m "add index"` → `flask db upgrade`
- [ ] **README.md** with: 專案簡介、架構圖、安裝步驟 (Python + Node)、API 文件、ER 圖連結、學習重點、Flask-Migrate 指令
- [ ] dbdiagram.io link in README
- [ ] Screenshots of working app (4 tabs)
- [ ] **Code comments 中文說明** — 每個 function docstring、關鍵邏輯註解、TypeScript interfaces
- [ ] Verify assignment requirements met"""

new_phases = """## 8. Implementation Phases

### Phase 1: Backend Setup + Database Migrations (Day 1)
- [ ] Create Python virtualenv: `python -m venv venv && source venv/bin/activate`
- [ ] Install deps: `pip install flask flask-sqlalchemy flask-migrate psycopg2-binary python-dotenv marshmallow pytest`
- [ ] Create `config.py` with `SQLALCHEMY_DATABASE_URI` from `.env` (dev + test DBs)
- [ ] Create `models/` with **all SQLAlchemy models** (Category, Supplier, Product, ProductSupplier, Location, StockItem, Salesperson, StockMovement)
- [ ] Create `app.py` with Flask app factory + `db.init_app(app)` + `Migrate(app, db)`
- [ ] Run `flask db init` → `flask db migrate -m "initial schema"` → `flask db upgrade`
- [ ] Verify tables in pgAdmin (AIlearn database) — check FKs, indexes, CHECK constraints
- [ ] Export ER diagram from pgAdmin or dbdiagram.io → `schema.md` (with Chinese column descriptions)

### Phase 2: Backend API + Services + Tests (Day 1-2)
- [ ] Implement `services/` (business logic: atomic transactions for stock in/out/transfer, validations, aggregations)
- [ ] Implement `schemas/` (marshmallow: request validation + response serialization for all entities)
- [ ] Implement `routes/` (Blueprints: products, categories, suppliers, locations, stock, alerts, salespeople, reports, dashboard)
- [ ] Register blueprints in `app.py` with `/api` prefix; configure CORS for Vite dev
- [ ] Implement `seeds/demo_data.py` + `flask seed-demo` CLI for teaching data
- [ ] Write `tests/` (pytest): unit tests for services, integration tests for routes, migration tests
- [ ] Test all 20+ endpoints with curl/Postman — verify transactions, FK constraints, report queries, edge cases

### Phase 3: React Frontend (Day 2)
- [ ] Initialize: `cd frontend && npm create vite@latest . -- --template react-ts`
- [ ] Install: `npm install && npm install axios @tanstack/react-query tailwindcss @tailwindcss/vite recharts react-router-dom @headlessui/react && npx tailwindcss init`
- [ ] Configure Vite proxy to Flask (`/api` → `http://localhost:5000`) in `vite.config.ts`
- [ ] Build `api/client.ts` (Axios with interceptors for auth/error handling) + `api/endpoints.ts`
- [ ] Create custom hooks: `useProducts`, `useCategories`, `useSuppliers`, `useLocations`, `useStock`, `useSalespeople`, `useReports`, `useDashboard`
- [ ] Build 5 page components: `DashboardPage`, `ProductsPage`, `CategoriesSuppliersLocationsPage`, `StockPage`, `AlertsPage`, `ReportsPage`
- [ ] Shared UI components: `DataTable` (sort/filter/page), `Modal`, `Form`, `KPICard`, `Chart` (Recharts), `CategoryTree`, `LocationTree`, `Toast`
- [ ] Style with Tailwind CSS (responsive, dark mode ready, accessible)
- [ ] Implement TanStack Query: `staleTime: 30s`, `refetchOnWindowFocus: false`, optimistic updates for stock

### Phase 4: Integration + Polish + Documentation (Day 2-3)
- [ ] End-to-end testing (Dashboard → Products → Stock In/Out/Transfer → Alerts → Reports → Leaderboard)
- [ ] Verify Flask-Migrate: `flask db migrate -m "add supplier lead_time"` → `flask db upgrade`
- [ ] Run full test suite: `pytest` (backend) + `npm test` (frontend)
- [ ] **README.md** with: 專案簡介、架構圖、安裝步驟 (Python + Node)、API 文件、ER 圖連結、學習重點、Flask-Migrate 指令、Seed 指令
- [ ] dbdiagram.io link in README
- [ ] Screenshots of working app (5 tabs + dashboard)
- [ ] **Code comments 中文說明** — 每個 function docstring、關鍵邏輯註解、TypeScript interfaces、Trade-off 註解
- [ ] Verify assignment requirements met (checklist in Appendix)"""

if old_phases in content:
    content = content.replace(old_phases, new_phases)
    print("Phases updated!")
else:
    print("Phases NOT FOUND")

with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'w', encoding='utf-8') as f:
    f.write(content)