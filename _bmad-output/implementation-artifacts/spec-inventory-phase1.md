---
title: 'Inventory Management System - Phase 1: Backend Setup & Database Migrations'
type: 'feature'
created: '2026-10-21'
status: 'draft'
route: ''
review_loop_iteration: 0
context: []
---

<frozen-after-approval reason="human-owned intent — do not modify unless human renegotiates">

## Intent

**Problem:** No backend exists. Need to initialize a Flask project with Flask-SQLAlchemy, Flask-Migrate (Alembic), and all SQLAlchemy models for the inventory management system. The database must connect to the existing PostgreSQL `AIlearn` database on localhost:5432 with user `postgres` and password `dark2204`.

**Approach:** Create a Flask app factory with SQLAlchemy ORM models for all 8 tables (Category, Supplier, Product, ProductSupplier, Location, StockItem, Salesperson, StockMovement), configure Flask-Migrate for version-controlled migrations, and run the initial migration against the `AIlearn` database. Add a seed CLI command for demo data.

## Boundaries & Constraints

**Always:**
- Use Flask app factory pattern (`create_app()`)
- SQLAlchemy 2.x style models with type hints
- Flask-Migrate (Alembic) for ALL schema changes — never `db.create_all()`
- PostgreSQL `AIlearn` database on localhost:5432, user `postgres`, password `dark2204`
- Models must match the PRD: 8 tables with proper FKs, indexes, CHECK constraints
- Environment config via `.env` and `.flaskenv`
- Virtualenv in `venv/` (gitignored)

**Never:**
- No `db.create_all()` in production code
- No hardcoded DB credentials in code
- No raw SQL for schema (use Alembic migrations)
- No auth for this assignment (per PRD)
- No hard delete — use `is_active` soft deletes
- No `ON DELETE CASCADE` on Product → StockMovement (use RESTRICT for audit trail)

## I/O & Edge-Case Matrix

| Scenario | Input / State | Expected Output / Behavior | Error Handling |
|----------|--------------|---------------------------|----------------|
| HAPPY_PATH | `flask db init` → `flask db migrate` → `flask db upgrade` | Migration files created, tables exist in `AIlearn` | N/A |
| DB_CONNECT_FAIL | PostgreSQL not running / wrong credentials | Clear error message, exit code != 0 | Log connection error, suggest `pg_isready` |
| MIGRATE_CONFLICT | Multiple heads in migrations | Alembic detects conflict, requires manual resolution | `flask db heads` shows conflict |
| SEED_DEMO | `flask seed-demo --password X` | 3 demo accounts + sample categories, suppliers, products, salespeople | Rollback on error, idempotent |

## Open Questions

- CHOICE: Should demo data include multi-location stock (Location + StockItem) or just single-location? — options: A) Single location only (simpler) / B) Multi-location with StockItem (matches full model, more demo data)
- CHOICE: Should the initial migration include all 8 tables or split into 2 migrations (core + extended)? — options: A) Single migration (all tables at once) / B) Two migrations: core (Category, Supplier, Product, Salesperson) + extended (Location, StockItem, ProductSupplier, StockMovement)

</frozen-after-approval>

## Code Map

- `config.py` -- Configuration loading from `.env` (SQLALCHEMY_DATABASE_URI, SECRET_KEY)
- `models/__init__.py` -- `db = SQLAlchemy()` instance export
- `models/category.py` -- Category model (hierarchical, parent_id, path)
- `models/supplier.py` -- Supplier model (lead_time_days, contact)
- `models/product.py` -- Product model (SKU, barcode, pricing, inventory fields)
- `models/product_supplier.py` -- ProductSupplier association (supplier_sku, price)
- `models/location.py` -- Location model (hierarchical warehouses)
- `models/stock_item.py` -- StockItem per-location quantity
- `models/salesperson.py` -- Salesperson model (employee_id, hire_date)
- `models/stock_movement.py` -- StockMovement append-only ledger (RESTRICT on product)
- `app.py` -- Flask app factory, db.init_app, Migrate, blueprint registration
- `migrations/env.py` -- Alembic environment (target_metadata = db.metadata)
- `seeds/demo_data.py` -- Demo data creation logic
- `seeds/cli.py` -- `flask seed-demo` command registration
- `.env` -- DB credentials (gitignored)
- `.flaskenv` -- FLASK_APP, FLASK_ENV

## Tasks & Acceptance

**Execution:**
- [ ] `config.py` -- Create config class with SQLALCHEMY_DATABASE_URI from env, SECRET_KEY, SQLALCHEMY_TRACK_MODIFICATIONS=False -- Centralized config
- [ ] `models/__init__.py` -- Export `db = SQLAlchemy()` and `init_db(app)` helper -- Single SQLAlchemy instance
- [ ] `models/category.py` -- Category model with parent_id, path, children relationship -- Hierarchical categories
- [ ] `models/supplier.py` -- Supplier model with lead_time_days, is_active -- Supplier management
- [ ] `models/product.py` -- Product model with SKU, barcode, pricing, inventory, relationships -- Core product entity
- [ ] `models/product_supplier.py` -- ProductSupplier association with supplier_sku, supplier_price -- Many-to-many with supplier data
- [ ] `models/location.py` -- Location model with parent_id, path -- Hierarchical locations
- [ ] `models/stock_item.py` -- StockItem with product_id, location_id, quantity, reserved, batch_number -- Per-location stock
- [ ] `models/salesperson.py` -- Salesperson with employee_id, hire_date, is_active -- Sales attribution
- [ ] `models/stock_movement.py` -- StockMovement with RESTRICT on product, price snapshot, reference fields -- Append-only ledger
- [ ] `app.py` -- Flask factory, config, db.init_app, Migrate(app, db), blueprint registration -- App entry point
- [ ] `.env` -- DATABASE_URL, SECRET_KEY (gitignored) -- Credentials
- [ ] `.flaskenv` -- FLASK_APP=app.py, FLASK_ENV=development -- Dev config
- [ ] `seeds/demo_data.py` -- create_demo_data() with categories, suppliers, products, salespeople, locations, stock items -- Demo data
- [ ] `seeds/cli.py` -- register_seed_commands(app) with `flask seed-demo --password` -- CLI command
- [ ] `flask db init` -- Initialize migrations directory -- Migration setup
- [ ] `flask db migrate -m "initial schema"` -- Generate initial migration -- Alembic migration
- [ ] `flask db upgrade` -- Apply migration to AIlearn -- Schema creation
- [ ] `flask seed-demo --password test123` -- Populate demo data -- Teaching data

**Acceptance Criteria:**
- Given PostgreSQL running on localhost:5432 with AIlearn database, when running `flask db upgrade`, then all 8 tables exist in pgAdmin with correct columns, FKs, indexes, CHECK constraints
- Given fresh venv with dependencies installed, when running `flask db init` then `flask db migrate`, then `migrations/versions/` contains one migration file with all 8 tables
- Given migration applied, when running `flask seed-demo --password test123`, then demo categories, suppliers, products, salespeople, locations, and stock items exist in DB
- Given app factory imported, when calling `create_app()`, then Flask app has `db`, `migrate`, and all blueprints registered

## Implementation Notes

## Spec Change Log

## Review Triage Log

## Design Notes

**Why Flask App Factory:** Enables testing with different configs, supports multiple app instances, standard Flask pattern.

**Why RESTRICT on Product→StockMovement:** Audit trail integrity — never allow product deletion if movements exist. Soft delete via `is_active=false`.

**Why Materialized `path` on Category/Location:** O(1) subtree queries vs recursive CTEs. Auto-maintained by service layer on create/update/move.

**Why Price Snapshot on StockMovement:** Historical accuracy for reports. `unit_price_at_time` immune to later price changes. Critical for salesperson performance reports.

**Why Per-Location StockItem:** Separates logical product from physical stock. Enables multi-warehouse. `current_stock` = SUM(StockItem.quantity) computed or denormalized.

**Migration Strategy:** Single initial migration for simplicity. Future changes use `flask db migrate -m "description"`.

## Verification

**Commands:**
- `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt` -- expected: virtualenv ready with all deps
- `flask db init` -- expected: `migrations/` directory created with `env.py`, `script.py.mako`
- `flask db migrate -m "initial schema"` -- expected: `migrations/versions/xxxx_initial_schema.py` created with 8 tables
- `flask db upgrade` -- expected: tables visible in pgAdmin (AIlearn), no errors
- `flask seed-demo --password test123` -- expected: demo data inserted, no errors
- `python -c "from app import create_app; app = create_app(); print('OK')"` -- expected: app factory works

**Manual checks (if no CLI):**
- pgAdmin → AIlearn → Tables: category, supplier, product, product_supplier, location, stock_item, salesperson, stock_movement all present
- Each table has correct columns, FKs, indexes, CHECK constraints visible in pgAdmin
- `migrations/versions/` contains exactly one `.py` file with all 8 tables