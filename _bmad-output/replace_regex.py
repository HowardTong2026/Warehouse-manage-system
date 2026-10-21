import re

with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Use regex to find and replace the section
pattern = r'(## 5\. Technical Architecture\n\n```\n[\s\S]*?\n```\n\n\*\*Stack:\*\*\n[\s\S]*?\n- \*\*Controller:\*\* Flask routes in `routes/\*\.py` \(REST API\) \+ React custom hooks \(`useProducts`, `useStock`, `useReports`\))'

new_section = """## 5. Technical Architecture

**Architecture (from flask-react-inventory, adapted for PostgreSQL):**

```
DEVELOPMENT
React (port 5173) --Vite Proxy /api--> Flask (port 5000)
                                              |
                        SQLAlchemy ORM
                        Models -> Services -> Routes
                                              |
                        Flask-Migrate (Alembic)
                                              |
                        PostgreSQL (AIlearn)
```

**Production Deployment Pattern (flask-react-inventory):**
- `npm run build` -> `frontend/dist/`
- Flask serves static files + SPA fallback (index.html for client routes)
- /api/* always takes precedence
- Reverse proxy (nginx) -> Gunicorn -> Flask

**Stack (with specific versions from references):**
| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Backend | Flask | 3.x | Web framework |
| | Flask-SQLAlchemy | 3.x | ORM |
| | Flask-Migrate | 4.x | Alembic migrations |
| | Marshmallow | 3.x | Validation/serialization |
| | psycopg2-binary | 2.9+ | PostgreSQL driver |
| | python-dotenv | 1.x | Env config |
| | pytest | 7.x | Testing |
| Database | PostgreSQL | 18 | Primary DB |
| Frontend | React | 18.x | UI library |
| | TypeScript | 5.x | Type safety |
| | Vite | 5.x | Build/dev server |
| | Tailwind CSS | 3.x | Styling |
| | Axios | 1.7+ | HTTP client |
| | TanStack Query | 5.x | Server state cache |
| | React Router | 6.x | Client routing |
| | Recharts / Chart.js | - | Charts for reports |
| DevOps | ruff | - | Python lint/format |
| | ESLint + Prettier | - | TS/JS lint/format |
| | pre-commit | - | Git hooks |

**MVC/MVVM Mapping (per PPTX + flask-react-inventory):**
| Pattern | Backend (Flask) | Frontend (React) |
|---------|-----------------|------------------|
| Model | models/*.py (SQLAlchemy) + services/*_service.py (business logic, transactions) | types/index.ts (interfaces) + hooks/use*.ts (server state) |
| View | API only | components/ (UI primitives) + pages/*.tsx (composed views) |
| Controller | routes/*.py (Blueprints, request/response) | hooks/use*.ts (mutations, queries) + event handlers in components |

**Key Architectural Decisions:**
- Service layer owns transactions -- routes are thin; services handle DB commits/rollbacks
- Append-only StockMovement -- ON DELETE RESTRICT on product; never mutate history
- Price snapshots -- unit_price_at_time on every movement
- Marshmallow schemas -- single source of truth for validation + serialization
- TanStack Query -- server state caching, deduping, background refetch
- Vite proxy -- seamless /api -> Flask in dev; no CORS issues"""

# Replace using regex
new_content, count = re.subn(pattern, new_section, content, flags=re.MULTILINE)

with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\match_result2.txt', 'w', encoding='utf-8') as f:
    f.write("Replacements: " + str(count) + "\n")
    if count > 0:
        f.write("SUCCESS!\n")
    else:
        f.write("FAILED: Pattern not found\n")

if count > 0:
    with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'w', encoding='utf-8') as f:
        f.write(new_content)