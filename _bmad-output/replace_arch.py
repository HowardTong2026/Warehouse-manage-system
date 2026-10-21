with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'r', encoding='utf-8') as f:
    content = f.read()

old_section = """## 5. Technical Architecture

```
┌─────────────────┐     HTTP/REST      ┌─────────────────┐     SQL      ┌─────────────┐
│  Frontend       │ ◄─────────────────► │  Backend        │ ◄───────────► │  Database   │
│  (index.html)   │   fetch() / JSON    │  (Flask)        │  psycopg2    │  (PostgreSQL│
│  Vanilla JS     │                     │  app.py         │              │   AIlearn)  │
└─────────────────┘                     └─────────────────┘              └─────────────┘
                                               │
                                               ▼
                                     ┌─────────────────┐
                                     │  Services Layer │
                                     │  - product_svc  │
                                     │  - stock_svc    │
                                     │  - alert_svc    │
                                     │  - salesperson_svc│
                                     │  - report_svc   │  ← NEW: 業績報表
                                     └─────────────────┘
```

**Stack:**
- **Backend:** Python 3.10+, Flask 3.x, **Flask-SQLAlchemy**, **Flask-Migrate**, psycopg2-binary, python-dotenv
- **Database:** PostgreSQL 18 (running on localhost:5432, db: AIlearn, user: postgres) — **managed via Flask-Migrate migrations**
- **Frontend:** **React 18** (Vite + TypeScript), Tailwind CSS, **Axios** for API calls
- **Config:** `.env` for DB credentials; `flask` CLI for migrations

**Architecture Mapping (per PPTX):**
- **Model:** `models/*.py` (SQLAlchemy ORM) + `services/*_service.py` (business logic)
- **View:** React components in `frontend/src/components/` + `frontend/src/pages/`
- **Controller:** Flask routes in `routes/*.py` (REST API) + React custom hooks (`useProducts`, `useStock`, `useReports`)"""

new_section = """## 5. Technical Architecture

**Architecture (from flask-react-inventory, adapted for PostgreSQL):**

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DEVELOPMENT                                    │
│  ┌──────────────┐        Vite Proxy (/api)        ┌────────────────────┐   │
│  │   React      │ ◄──────────────────────────────► │      Flask         │   │
│  │  (port 5173) │    Axios + TanStack Query        │   (port 5000)      │   │
│  └──────────────┘                                 └─────────┬──────────┘   │
│                                                                │            │
└────────────────────────────────────────────────────────────────│────────────┘
                                                                 │
                                              ┌──────────────────▼─────────────┐
                                              │      SQLAlchemy ORM            │
                                              │  Models → Services → Routes    │
                                              └──────────────────┬─────────────┘
                                                                 │
                                              ┌──────────────────▼─────────────┐
                                              │    Flask-Migrate (Alembic)     │
                                              │  migrations/versions/*.py      │
                                              └──────────────────┬─────────────┘
                                                                 │
                                              ┌──────────────────▼─────────────┐
                                              │      PostgreSQL (AIlearn)      │
                                              │  Tables, FKs, Indexes, CHECKs  │
                                              └────────────────────────────────┘
```

**Production Deployment Pattern (flask-react-inventory):**
- `npm run build` → `frontend/dist/`
- Flask serves static files + SPA fallback (`index.html` for client routes)
- `/api/*` always takes precedence
- Reverse proxy (nginx) → Gunicorn → Flask

**Stack (with specific versions from references):**
| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Backend** | Flask | 3.x | Web framework |
| | Flask-SQLAlchemy | 3.x | ORM |
| | Flask-Migrate | 4.x | Alembic migrations |
| | Marshmallow | 3.x | Validation/serialization |
| | psycopg2-binary | 2.9+ | PostgreSQL driver |
| | python-dotenv | 1.x | Env config |
| | pytest | 7.x | Testing |
| **Database** | PostgreSQL | 18 | Primary DB |
| **Frontend** | React | 18.x | UI library |
| | TypeScript | 5.x | Type safety |
| | Vite | 5.x | Build/dev server |
| | Tailwind CSS | 3.x | Styling |
| | Axios | 1.7+ | HTTP client |
| | TanStack Query | 5.x | Server state cache |
| | React Router | 6.x | Client routing |
| | Recharts / Chart.js | - | Charts for reports |
| **DevOps** | ruff | - | Python lint/format |
| | ESLint + Prettier | - | TS/JS lint/format |
| | pre-commit | - | Git hooks |

**MVC/MVVM Mapping (per PPTX + flask-react-inventory):**
| Pattern | Backend (Flask) | Frontend (React) |
|---------|-----------------|------------------|
| **Model** | `models/*.py` (SQLAlchemy) + `services/*_service.py` (business logic, transactions) | `types/index.ts` (interfaces) + `hooks/use*.ts` (server state) |
| **View** | — (API only) | `components/` (UI primitives) + `pages/*.tsx` (composed views) |
| **Controller** | `routes/*.py` (Blueprints, request/response) | `hooks/use*.ts` (mutations, queries) + event handlers in components |

**Key Architectural Decisions:**
- **Service layer owns transactions** — routes are thin; services handle DB commits/rollbacks
- **Append-only StockMovement** — `ON DELETE RESTRICT` on product; never mutate history
- **Price snapshots** — `unit_price_at_time` on every movement
- **Marshmallow schemas** — single source of truth for validation + serialization
- **TanStack Query** — server state caching, deduping, background refetch
- **Vite proxy** — seamless `/api` → Flask in dev; no CORS issues"""

if old_section in content:
    content = content.replace(old_section, new_section)
    with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS!")
else:
    print("OLD SECTION NOT FOUND")
    # Debug: show what we're looking for
    idx = content.find("## 5. Technical Architecture")
    next_idx = content.find("\n## ", idx + 1)
    actual = content[idx:next_idx]
    print("ACTUAL:")
    print(repr(actual[:200]))
    print("EXPECTED:")
    print(repr(old_section[:200]))