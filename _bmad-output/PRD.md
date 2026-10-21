# PRD: Inventory Management System (庫存管理系統)

**Document Version:** 1.1  
**Date:** 2026-10-21  
**Author:** BMAD Product Manager (John)  
**Project:** AI學習第八課 — 庫存管理課題  
**Status:** Draft for Review

---

## 1. Executive Summary

### 1.1 Product Vision
Build a functional inventory management web application demonstrating CRUD operations, database design, and REST API implementation — suitable as a **course teaching assignment** showcasing full-stack development skills with **PostgreSQL, Flask (SQLAlchemy + Flask-Migrate), React 18 + TypeScript + Tailwind CSS**. Code must be clean, well-documented, and pedagogically clear — serving as a reference implementation for MVC/MVVM architecture.

### 1.2 Problem Statement
Students need a practical project that demonstrates:
- Database schema design (ER diagram → SQLAlchemy models → Flask-Migrate migrations → PostgreSQL)
- RESTful API design (CRUD ↔ SQL ↔ HTTP mapping) with proper validation, transactions, and error handling
- Frontend-backend integration (React hooks ↔ Flask Blueprints) with Vite proxy dev setup
- Real-world domain: **inventory tracking with low-stock alerts** + **salesperson performance analysis**
- Industry best practices: append-only stock ledger, price snapshots, role-based access, migrations

### 1.3 Target Users
- **Primary:** Course instructor / grader evaluating the assignment
- **Secondary:** Portfolio reviewers (future employers)
- **Tertiary:** The student (learning artifact — code must be readable, commented, educational)

### 1.4 Reference Systems Studied
| System | Stars | Stack | Key Patterns Adopted |
|--------|-------|-------|---------------------|
| **InvenTree** | 7.7k | Django + REST API | Hierarchical categories, suppliers, BOM, builds, stock locations, serialization, plugin system |
| **flask-react-inventory** | Course project | Flask + React + SQLAlchemy + Alembic | Service layer transactions, append-only stock_movements, role-based access, Alembic migrations, TanStack Query |
| **inventory-manager** | 1 | Flask + React + MySQL | Multi-warehouse, product movements, validation patterns, Material UI |

---

## 2. User Stories & Requirements

### 2.1 Epic: Product Catalog Management
| ID | User Story | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| US-1.1 | As a user, I can add a product with name, SKU, category, unit price, and reorder threshold so that I can track inventory items. | Must | POST /api/products creates product; returns 201 with product JSON; SKU uniqueness enforced |
| US-1.2 | As a user, I can list all products so that I can see the catalog. | Must | GET /api/products returns array of products with current_stock |
| US-1.3 | As a user, I can update a product's details so that I can correct errors. | Must | PUT /api/products/:id updates fields; returns updated product |
| US-1.4 | As a user, I can delete a product so that I can remove discontinued items. | Must | DELETE /api/products/:id removes product; returns 204 |

### 2.2 Epic: Stock Movement Tracking
| ID | User Story | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| US-2.1 | As a user, I can record stock-in (receiving inventory) so that stock quantity increases. | Must | POST /api/stock/in {product_id, quantity, reason} increments product.current_stock; creates stock_movement record with type='in' |
| US-2.2 | As a user, I can record stock-out (sales/adjustments) **with salesperson attribution** so that stock quantity decreases and sales are tracked per salesperson. | Must | POST /api/stock/out {product_id, quantity, reason?, salesperson_id} decrements product.current_stock; validates stock ≥ 0; creates stock_movement record with type='out' and salesperson_id |
| US-2.3 | As a user, I can view stock movement history for a product so that I can audit changes. | Should | GET /api/products/:id/movements returns paginated movement log with salesperson info |

### 2.3 Epic: Low-Stock Alerting (隨時知道那些品項需要補貨)
| ID | User Story | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| US-3.1 | As a user, I can **at any time** see products below reorder threshold so that I know what to restock immediately. | Must | GET /api/alerts/low-stock returns products where current_stock ≤ reorder_threshold; real-time (no caching) |
| US-3.2 | As a user, I see a visual indicator on the dashboard for low-stock items. | Must | Frontend highlights low-stock rows in red; sticky alert banner shows count |
| US-3.3 | As a user, I can filter/sort products by stock status so that restock priority is clear. | Should | Table sortable by current_stock, threshold, status |

### 2.4 Epic: Salesperson Performance (查看每個銷貨員的業績)
| ID | User Story | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| US-4.1 | As a manager, I can manage salespeople (CRUD) so that sales can be attributed. | Must | CRUD endpoints for /api/salespeople |
| US-4.2 | As a cashier/salesperson, I record a sale with my ID so that my performance is tracked. | Must | POST /api/stock/out requires salesperson_id; validates salesperson exists |
| US-4.3 | As a manager, I can view **each salesperson's performance**: total sales amount, number of transactions, top products sold, for any date range. | Must | GET /api/reports/salesperson/:id?from=&to= returns {total_amount, transaction_count, top_products[], daily_breakdown[]} |
| US-4.4 | As a manager, I can view a **leaderboard** of all salespeople ranked by revenue. | Must | GET /api/reports/salespeople/leaderboard?from=&to= returns ranked list |
| US-4.4 | As a manager, I can export salesperson performance to CSV. | Could | GET /api/reports/salesperson/:id/export?format=csv |

### 2.5 Epic: Database & Documentation (教學用途)
| ID | User Story | Priority | Acceptance Criteria |
|----|------------|----------|---------------------|
| US-5.1 | As a developer, I have an ER diagram in dbdiagram.io so that the schema is documented. | Must | dbdiagram.io link in README; exports valid PostgreSQL SQL |
| US-5.2 | As a developer, I can initialize the database from SQL so that setup is reproducible. | Must | Running init.sql against AIlearn creates all tables, FKs, indexes |
| US-5.3 | As a developer, I have a schema.md documenting tables, columns, and relationships. | Must | Markdown file in _bmad-output/ |
| US-5.4 | As a student, the code is **well-commented, modular, and follows best practices** so that I can learn from it. | Must | Every function has docstring; separation of concerns; no magic numbers; README explains architecture |

---

## 3. Functional Requirements

### 3.1 Data Model (PostgreSQL + SQLAlchemy Models)

**Enhanced Schema** — incorporating best practices from InvenTree (hierarchical categories, suppliers, locations) and flask-react-inventory (append-only ledger, price snapshots, role-based access).

**Flask-SQLAlchemy Models** (used with Flask-Migrate for version-controlled schema):

```python
# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# models/category.py — InvenTree style: hierarchical categories
class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='SET NULL'), nullable=True)
    path = db.Column(db.String(500))  # materialized path for fast subtree queries (e.g. '1/5/12/')
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())
    
    parent = db.relationship('Category', remote_side=[id], back_populates='children')
    children = db.relationship('Category', back_populates='parent', cascade='all, delete-orphan')
    products = db.relationship('Product', back_populates='category')
    
    __table_args__ = (db.UniqueConstraint('name', 'parent_id', name='uq_category_name_parent'),)

# models/supplier.py — InvenTree: supplier management
class Supplier(db.Model):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, unique=True)
    contact_name = db.Column(db.String(100))
    email = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    lead_time_days = db.Column(db.Integer, default=7)  # for reorder planning
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())
    
    product_suppliers = db.relationship('ProductSupplier', back_populates='supplier', cascade='all, delete-orphan')

# models/product.py — enhanced with supplier links, barcode, location
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    sku = db.Column(db.String(50), nullable=False, unique=True)  # internal SKU
    barcode = db.Column(db.String(100), unique=True)  # EAN/UPC/ISBN
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='SET NULL'))
    
    # Pricing
    unit_price = db.Column(db.Numeric(12, 2), nullable=False)  # selling price
    cost_price = db.Column(db.Numeric(12, 2), default=0)  # for margin calc
    
    # Inventory
    reorder_threshold = db.Column(db.Integer, nullable=False, default=10)
    reorder_quantity = db.Column(db.Integer, nullable=False, default=50)  # suggested reorder qty
    current_stock = db.Column(db.Integer, nullable=False, default=0)
    reserved_stock = db.Column(db.Integer, nullable=False, default=0)  # allocated to pending orders
    available_stock = db.Column(db.Integer, nullable=False, default=0)  # computed: current - reserved
    
    # Tracking
    track_serial = db.Column(db.Boolean, default=False)  # InvenTree: serialized items
    track_batch = db.Column(db.Boolean, default=False)   # batch/lot tracking
    
    # Metadata
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())
    
    category = db.relationship('Category', back_populates='products')
    stock_movements = db.relationship('StockMovement', back_populates='product', cascade='all, delete-orphan')
    suppliers = db.relationship('ProductSupplier', back_populates='product', cascade='all, delete-orphan')
    stock_items = db.relationship('StockItem', back_populates='product', cascade='all, delete-orphan')  # per-location

# models/product_supplier.py — many-to-many with supplier-specific info
class ProductSupplier(db.Model):
    __tablename__ = 'product_supplier'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id', ondelete='CASCADE'), nullable=False)
    supplier_sku = db.Column(db.String(100))  # supplier's part number
    supplier_price = db.Column(db.Numeric(12, 2))  # purchase price
    min_order_qty = db.Column(db.Integer, default=1)
    is_preferred = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    
    product = db.relationship('Product', back_populates='suppliers')
    supplier = db.relationship('Supplier', back_populates='product_suppliers')
    
    __table_args__ = (db.UniqueConstraint('product_id', 'supplier_id', name='uq_product_supplier'),)

# models/location.py — InvenTree: hierarchical stock locations
class Location(db.Model):
    __tablename__ = 'location'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('location.id', ondelete='SET NULL'), nullable=True)
    path = db.Column(db.String(500))  # materialized path
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    
    parent = db.relationship('Location', remote_side=[id], back_populates='children')
    children = db.relationship('Location', back_populates='parent', cascade='all, delete-orphan')
    stock_items = db.relationship('StockItem', back_populates='location', cascade='all, delete-orphan')
    
    __table_args__ = (db.UniqueConstraint('name', 'parent_id', name='uq_location_name_parent'),)

# models/stock_item.py — per-location stock (InvenTree pattern)
class StockItem(db.Model):
    __tablename__ = 'stock_item'
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id', ondelete='CASCADE'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=0)
    reserved = db.Column(db.Integer, nullable=False, default=0)
    batch_number = db.Column(db.String(100))  # for batch tracking
    serial_numbers = db.Column(db.JSON)  # list of serial numbers if track_serial
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())
    
    product = db.relationship('Product', back_populates='stock_items')
    location = db.relationship('Location', back_populates='stock_items')
    
    __table_args__ = (db.UniqueConstraint('product_id', 'location_id', 'batch_number', name='uq_stock_item'),)

# models/salesperson.py
class Salesperson(db.Model):
    __tablename__ = 'salesperson'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(200), unique=True)
    phone = db.Column(db.String(20))
    employee_id = db.Column(db.String(50), unique=True)  # HR system ID
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    hire_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), onupdate=db.func.now())
    
    stock_movements = db.relationship('StockMovement', back_populates='salesperson')

# models/stock_movement.py — append-only ledger (flask-react-inventory pattern)
class StockMovement(db.Model):
    __tablename__ = 'stock_movement'
    id = db.Column(db.BigInteger, primary_key=True)
    
    # References
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='RESTRICT'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id', ondelete='SET NULL'))
    salesperson_id = db.Column(db.Integer, db.ForeignKey('salesperson.id', ondelete='SET NULL'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id', ondelete='SET NULL'))  # for stock-in
    
    # Movement details
    type = db.Column(db.String(20), nullable=False)  # 'in', 'out', 'adjustment', 'transfer', 'return'
    reference_type = db.Column(db.String(20))  # 'sale', 'purchase', 'adjustment', 'transfer'
    reference_id = db.Column(db.Integer)  # links to sale/purchase/adjustment record
    
    # Quantities
    quantity = db.Column(db.Integer, nullable=False)  # positive for in, negative for out
    unit_price_at_time = db.Column(db.Numeric(12, 2), nullable=False)  # price snapshot
    total_amount = db.Column(db.Numeric(12, 2))  # quantity * unit_price_at_time
    
    # Context
    reason = db.Column(db.String(500))
    notes = db.Column(db.Text)
    changed_by = db.Column(db.String(100))  # username or system
    
    # Timestamp
    created_at = db.Column(db.DateTime(timezone=True), server_default=db.func.now(), index=True)
    
    # Relationships
    product = db.relationship('Product', back_populates='stock_movements')
    location = db.relationship('Location')
    salesperson = db.relationship('Salesperson', back_populates='stock_movements')
    supplier = db.relationship('Supplier')
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint("type IN ('in', 'out', 'adjustment', 'transfer', 'return')", name='ck_movement_type'),
        db.CheckConstraint('quantity != 0', name='ck_movement_quantity_nonzero'),
    )
```

**Key Design Decisions from References:**

| Pattern | Source | Why |
|---------|--------|-----|
| **Hierarchical categories/locations** | InvenTree | Supports unlimited nesting; `path` column enables fast subtree queries |
| **ProductSupplier many-to-many** | InvenTree | Multiple suppliers per product; supplier-specific SKU/price |
| **StockItem per location** | InvenTree | Multi-warehouse ready; separates logical product from physical stock |
| **Append-only StockMovement** | flask-react-inventory | Never update/delete movements; audit trail; `RESTRICT` on product delete |
| **Price snapshot (unit_price_at_time)** | flask-react-inventory | Historical accuracy for reports; immune to price changes |
| **Reserved/available stock** | flask-react-inventory | Supports pending orders without overselling |
| **Serialization/batch fields** | InvenTree | Future-proof for regulated industries |
| **Materialized paths (path column)** | InvenTree | O(1) subtree queries vs recursive CTEs |

**PostgreSQL DDL Highlights** (generated by Flask-Migrate):

```sql
-- Key indexes for report performance
CREATE INDEX idx_stock_movement_product_created ON stock_movement(product_id, created_at DESC);
CREATE INDEX idx_stock_movement_salesperson_created ON stock_movement(salesperson_id, created_at DESC);
CREATE INDEX idx_stock_movement_type_created ON stock_movement(type, created_at DESC);
CREATE INDEX idx_stock_movement_reference ON stock_movement(reference_type, reference_id);

-- Composite indexes for dashboard queries
CREATE INDEX idx_product_category_active ON product(category_id, is_active);
CREATE INDEX idx_stock_item_location_product ON stock_item(location_id, product_id);

-- CHECK constraints enforced at DB level
ALTER TABLE product ADD CONSTRAINT ck_product_price CHECK (unit_price >= 0);
ALTER TABLE product ADD CONSTRAINT ck_product_stock CHECK (current_stock >= 0);
ALTER TABLE stock_movement ADD CONSTRAINT ck_movement_qty CHECK (quantity != 0);
```

### 3.2 REST API Specification

**Design follows flask-react-inventory patterns:** Blueprint-based, Marshmallow validation, consistent error format, pagination, filtering, sorting.

| Method | Endpoint | Description | Query Params | Request Body | Response |
|--------|----------|-------------|--------------|--------------|----------|
| **Products** |
| GET | /api/products | List products with pagination, filter, sort | `page`, `limit`, `search`, `category_id`, `is_active`, `low_stock`, `sort_by`, `sort_dir` | — | 200: `{items: [...], total, page, pages}` |
| GET | /api/products/:id | Get single product with stock details | — | — | 200: product + stock_items + movements summary |
| POST | /api/products | Create product | — | `{name, sku, barcode?, description?, category_id?, unit_price, cost_price?, reorder_threshold?, reorder_quantity?, track_serial?, track_batch?}` | 201: created product |
| PUT | /api/products/:id | Update product | — | partial product fields | 200: updated product |
| DELETE | /api/products/:id | Soft delete (is_active=false) | — | — | 204 |
| **Categories** |
| GET | /api/categories | Tree or flat list | `tree=true` | — | 200: nested or flat categories |
| POST | /api/categories | Create category | — | `{name, description?, parent_id?}` | 201: created |
| PUT | /api/categories/:id | Update category | — | partial fields | 200: updated |
| **Suppliers** |
| GET | /api/suppliers | List suppliers | `page`, `limit`, `is_active` | — | 200: paginated |
| POST | /api/suppliers | Create supplier | — | `{name, contact_name?, email?, phone?, address?, lead_time_days?}` | 201: created |
| PUT | /api/suppliers/:id | Update supplier | — | partial fields | 200: updated |
| POST | /api/products/:id/suppliers | Link supplier to product | — | `{supplier_id, supplier_sku?, supplier_price?, min_order_qty?, is_preferred?}` | 201: link |
| **Locations** |
| GET | /api/locations | Tree or flat | `tree=true` | — | 200: nested/flat locations |
| POST | /api/locations | Create location | — | `{name, description?, parent_id?}` | 201: created |
| **Stock Items (per-location)** |
| GET | /api/products/:id/stock | Stock across locations | — | — | 200: `[{location, quantity, reserved, available}]` |
| POST | /api/stock/adjust | Adjust stock at location | — | `{product_id, location_id, quantity_delta, reason?, batch_number?}` | 201: movement |
| **Stock Movements** |
| POST | /api/stock/in | Receive stock (purchase) | — | `{product_id, location_id, quantity, unit_price, supplier_id?, reason?, reference_id?}` | 201: movement + updated stock |
| POST | /api/stock/out | **Record sale** (stock-out + salesperson) | — | `{product_id, location_id, quantity, unit_price, salesperson_id, reason?, reference_type:'sale', reference_id?}` | 201: movement + updated stock |
| POST | /api/stock/transfer | Transfer between locations | — | `{product_id, from_location_id, to_location_id, quantity, reason?}` | 201: two movements (out+in) |
| GET | /api/products/:id/movements | Paginated movement history | `page`, `limit`, `type`, `from`, `to` | — | 200: `{items: [...], total}` |
| **Alerts** |
| GET | /api/alerts/low-stock | Real-time low stock | `include_zero=false` | — | 200: products with `current_stock ≤ reorder_threshold` |
| GET | /api/alerts/reorder-suggestions | Suggested purchase orders | — | — | 200: grouped by supplier with totals |
| **Salespeople** |
| GET | /api/salespeople | List | `page`, `limit`, `is_active` | — | 200: paginated |
| POST | /api/salespeople | Create | — | `{name, email?, phone?, employee_id?, hire_date?}` | 201: created |
| PUT | /api/salespeople/:id | Update | — | partial fields | 200: updated |
| DELETE | /api/salespeople/:id | Deactivate (soft) | — | — | 204 |
| **Reports (Salesperson Performance)** |
| GET | /api/reports/salesperson/:id | **Individual performance** | `from`, `to`, `group_by: day\|week\|month` | — | 200: `{summary, top_products, daily_breakdown, transactions[]}` |
| GET | /api/reports/salespeople/leaderboard | **All salespeople ranked** | `from`, `to`, `metric: revenue\|transactions\|avg_order` | — | 200: `[{rank, salesperson, total_revenue, transactions, avg_order}]` |
| GET | /api/reports/salesperson/:id/export | CSV export | `from`, `to` | — | 200: `text/csv` |
| **Dashboard** |
| GET | /api/dashboard/summary | KPIs for overview | — | — | 200: `{total_products, low_stock_count, total_stock_value, today_sales, today_transactions, top_salespeople[]}` |

**Error Response Format (consistent):**
```json
{
  "error": "VALIDATION_ERROR|NOT_FOUND|CONFLICT|SERVER_ERROR",
  "message": "Human-readable description",
  "details": {"field": "specific issue"}  // for validation errors
}
```

**Pagination Response Wrapper:**
```json
{
  "items": [...],
  "total": 150,
  "page": 1,
  "limit": 20,
  "pages": 8
}
```

### 3.3 Business Rules
**Core rules (from flask-react-inventory & InvenTree):**

1. **SKU/barcode uniqueness:** `product.sku` and `product.barcode` unique (DB constraints)
2. **Stock never negative:** `stock_out`/`transfer` fails 400 if `available_stock < quantity`; `available_stock = current_stock - reserved_stock`
3. **Append-only ledger:** `StockMovement` records **never updated or deleted** (`ON DELETE RESTRICT` on product); audit trail integrity
4. **Price snapshot:** `unit_price_at_time` captured at movement time; immune to later price changes
5. **Atomic transactions:** Stock update + movement insert in single DB transaction (service layer)
6. **Sales attribution:** Every `type='out'` with `reference_type='sale'` **must** have valid active `salesperson_id`
7. **Reorder logic:** `low_stock` when `available_stock ≤ reorder_threshold`; `reorder_quantity` suggests PO qty
8. **Soft deletes:** Product, Category, Supplier, Salesperson, Location use `is_active=false` (not hard delete)
9. **Hierarchical paths:** Category/Location `path` auto-maintained (e.g. `'1/5/12/'`) for O(1) subtree queries
10. **Reserved stock:** `reserved_stock` incremented on sale draft, decremented on completion/cancellation
11. **Multi-location:** Stock tracked per `StockItem(product_id, location_id)`; `current_stock` = SUM(stock_items.quantity)
12. **Real-time alerts:** `/api/alerts/low-stock` queries live data (no caching/materialized views)

**Validation Rules (Marshmallow schemas):**
- SKU: alphanumeric + dash/underscore, 3-50 chars
- Barcode: EAN-13, UPC-A, ISBN-13 format validation
- Email: RFC 5322 compliant
- Quantities: positive integers
- Prices: 2 decimal places, non-negative
- Dates: ISO 8601 (YYYY-MM-DD)

---

## 4. Non-Functional Requirements (教學導向)

| Category | Requirement |
|----------|-------------|
| **Performance** | API < 200ms single; < 500ms list (1000 items); reports < 1s; React initial load < 3s; TanStack Query caching |
| **Reliability** | Atomic transactions (stock + movement); append-only ledger; DB CHECK constraints; FK `RESTRICT` on product |
| **Security** | No auth for assignment; parameterized queries (SQLAlchemy ORM); Marshmallow validation; CORS configured; rate limiting ready |
| **Usability** | React + Tailwind responsive UI; keyboard navigation; ARIA labels; loading/error states; toast notifications |
| **Maintainability** | Blueprint routes → Service layer → SQLAlchemy models; Marshmallow schemas; each module < 200 lines; type hints |
| **Portability** | Windows/macOS/Linux; Python 3.10+; Node 18+; PostgreSQL 14+; Docker-ready |
| **Testing** | pytest backend (unit + integration); Vitest frontend; test DB separate (`_test` suffix); CI-ready |
| **Educational Value (教學用途)** | Docstrings + type hints; no magic numbers; comments explain "why"; MVC/MVVM mapped; README with architecture; migration history; seed/demo data script |
| **DevEx** | Vite proxy (`/api` → Flask); hot reload both ends; `flask db` CLI; `npm run dev`; pre-commit hooks (ruff, eslint) |

---

## 5. Technical Architecture

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
- Vite proxy -- seamless /api -> Flask in dev; no CORS issues

---

## 6. UI/UX Specification

### 6.1 Tab Layout (5 Tabs for Complete Teaching Coverage)
| Tab | Section | Components |
|-----|---------|------------|
| **📦 產品管理** | Header | Title: "Inventory Management" + "Add Product" button |
| | Filters | Search, Category dropdown, Active only, Low-stock only |
| | Main Table | Columns: SKU, Barcode, Name, Category (hierarchical), Price, Cost, Stock, Threshold, **Status**, Actions |
| | Status Badge | Green "OK" / **Red "LOW STOCK — 需補貨"** (available_stock ≤ threshold) |
| | Add/Edit Modal | Tabs: Basic, Pricing, Inventory, Suppliers; Form with all fields |
| | Category Tree | Collapsible sidebar (InvenTree style) for hierarchical navigation |
| **🏷️ 分類/供應商/倉位** | Category Tree | Drag-drop reorder; create/edit/delete with parent selector |
| | Supplier Table | CRUD modal; lead time, contact info, active toggle |
| | Supplier Link Modal | Link product↔supplier with supplier_sku, price, min_order_qty |
| | Location Tree | Hierarchical warehouses/zones/bins (InvenTree style) |
| **📥 進貨/銷貨** | Stock In Modal | Product (searchable), Location, Quantity, Unit Price, Supplier dropdown, Reason, Batch# |
| | Stock Out Modal | Product, Location, Quantity, **Salesperson (required)**, Reason, Batch/Serial |
| | Transfer Modal | Product, From Location, To Location, Quantity, Reason |
| | Movement Log | Unified table: Date, Type, Product, Location, Qty, Price, Salesperson/Supplier, Reason, Batch |
| | Validation Toasts | Insufficient stock, missing salesperson, invalid quantity |
| **🔔 補貨提醒** | Alert Banner | **Sticky top: "⚠️ X 項需補貨 | Y 供應商建議採購" — click to jump** |
| | Low-Stock Table | Products with available ≤ threshold; urgency = (threshold - available) / threshold |
| | Reorder Suggestions | Grouped by Supplier: Product, Current, Threshold, Suggested Qty, Est. Cost |
| | One-Click PO | "Generate PO" button → pre-filled purchase order per supplier |
| **👥 業績報表** | KPI Cards | Total Revenue, Transactions, Avg Order, Top Salesperson (period) |
| | Salesperson Selector | Dropdown + Date Range (presets: Today, Week, Month, Custom) |
| | Performance Table | Product, Qty Sold, Revenue, Margin, Transactions |
| | Daily/Weekly/Monthly Chart | Recharts bar/line: Revenue, Transactions, Avg Order |
| | Leaderboard | Rank, Name, Revenue, Transactions, Avg Order, Conversion % |
| | Export | CSV/Excel buttons with date range |

### 6.2 Interaction Flow (Enhanced)
1. **Dashboard** → loads `/api/dashboard/summary` → KPI cards + low-stock count + today's sales
2. **產品管理** → search/filter → `GET /api/products?search=&category_id=&low_stock=true` → render table with hierarchical category badge
3. **Add Product** → modal tabs → `POST /api/products` → if suppliers linked, auto-create `ProductSupplier` rows
4. **分類/供應商/倉位** → category tree (lazy load children) → drag-drop → `PUT /api/categories/:id` with new parent
5. **Stock In** → select supplier → auto-fill supplier_price from `ProductSupplier` → `POST /api/stock/in` → updates `StockItem` + `StockMovement` + `Product.current_stock` in transaction
6. **Stock Out** → **must pick salesperson** → validates `available_stock` → `POST /api/stock/out` → atomic decrement + movement
7. **Transfer** → `POST /api/stock/transfer` → creates paired `out` + `in` movements in single transaction
8. **補貨提醒** → sticky banner count → click → filters product table → "Generate PO" → `GET /api/alerts/reorder-suggestions` grouped by supplier
9. **業績報表** → select salesperson + range → `GET /api/reports/salesperson/:id` → KPIs + chart + top products table
10. **Leaderboard** → `GET /api/reports/salespeople/leaderboard` → sortable table → click name → drill into individual report

### 6.3 Key UI Patterns from References
| Pattern | Source | Implementation |
|---------|--------|----------------|
| Hierarchical tree (categories/locations) | InvenTree | Recursive component with lazy loading; materialized path for O(1) subtree |
| Append-only movement log | flask-react-inventory | Immutable rows; filter by type/date; export CSV |
| Price snapshot display | flask-react-inventory | Show `unit_price_at_time` vs current `unit_price` in movement log |
| Supplier grouping for PO | InvenTree | Reorder suggestions auto-grouped by supplier with totals |
| TanStack Query caching | flask-react-inventory | `staleTime: 30s`; background refetch; optimistic updates for stock |
| Role-based visibility | flask-react-inventory | Admin sees cost/margin; Staff sees only own transactions |

---

## 7. Project Structure

```
AI學習第八課/
├── .env                      # DB credentials (gitignored)
├── .flaskenv                 # FLASK_APP, FLASK_ENV
├── config.py                 # Configuration (環境變數管理)
├── app.py                    # Flask app factory (create_app)
├── models/                   # SQLAlchemy models (Flask-Migrate 管理)
│   ├── __init__.py           # db = SQLAlchemy()
│   ├── category.py           # Hierarchical categories (parent_id, path)
│   ├── supplier.py           # Suppliers (lead_time, contact)
│   ├── product.py            # Product (SKU, barcode, pricing, inventory)
│   ├── product_supplier.py   # Many-to-many: product↔supplier (supplier_sku, price)
│   ├── location.py           # Hierarchical locations (warehouse/zone/bin)
│   ├── stock_item.py         # Per-location stock (quantity, reserved, batch, serial)
│   ├── salesperson.py        # Salespeople (employee_id, hire_date)
│   └── stock_movement.py     # Append-only ledger (price snapshot, refs)
├── migrations/               # Flask-Migrate 產生的遷移腳本 (git tracked)
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── services/                 # 業務邏輯層 (可單元測試)
│   ├── __init__.py
│   ├── product_service.py
│   ├── stock_service.py      # Atomic transactions for stock in/out/transfer
│   ├── alert_service.py      # Low-stock, reorder suggestions
│   ├── salesperson_service.py
│   ├── report_service.py     # Aggregations, leaderboards
│   └── supplier_service.py
├── routes/                   # REST API 路由 (Blueprint)
│   ├── __init__.py
│   ├── products.py
│   ├── categories.py
│   ├── suppliers.py
│   ├── locations.py
│   ├── stock.py
│   ├── alerts.py
│   ├── salespeople.py
│   └── reports.py
├── schemas/                  # 請求/響應驗證 (marshmallow)
│   ├── __init__.py
│   ├── product_schema.py
│   ├── category_schema.py
│   ├── supplier_schema.py
│   ├── location_schema.py
│   ├── stock_schema.py
│   ├── salesperson_schema.py
│   └── report_schema.py
├── seeds/                    # Demo/seed data for teaching
│   ├── __init__.py
│   ├── demo_data.py          # Sample categories, suppliers, products, salespeople
│   └── cli.py                # `flask seed-demo` command
├── tests/                    # Backend tests
│   ├── __init__.py
│   ├── conftest.py           # pytest fixtures (test DB, client)
│   ├── test_products.py
│   ├── test_stock.py
│   ├── test_reports.py
│   └── test_migrations.py
├── frontend/                 # React + Vite + TypeScript
│   ├── package.json
│   ├── vite.config.ts        # Proxy /api -> http://localhost:5000
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── index.html
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx           # Router + TanStack Query Provider
│   │   ├── api/
│   │   │   ├── client.ts      # Axios instance with baseURL, interceptors
│   │   │   └── endpoints.ts   # API endpoint constants
│   │   ├── hooks/
│   │   │   ├── useProducts.ts
│   │   │   ├── useCategories.ts
│   │   │   ├── useSuppliers.ts
│   │   │   ├── useLocations.ts
│   │   │   ├── useStock.ts
│   │   │   ├── useSalespeople.ts
│   │   │   ├── useReports.ts
│   │   │   └── useDashboard.ts
│   │   ├── components/
│   │   │   ├── layout/        # Sidebar, Header, Tabs
│   │   │   ├── ui/            # Button, Input, Select, Modal, Table, Badge, Toast
│   │   │   ├── products/      # ProductTable, ProductForm, CategoryTree
│   │   │   ├── stock/         # StockInModal, StockOutModal, TransferModal, MovementLog
│   │   │   ├── alerts/        # LowStockBanner, ReorderSuggestions, POGenerator
│   │   │   ├── reports/       # KPICards, Leaderboard, PerformanceChart, ExportButton
│   │   │   └── common/        # Loader, EmptyState, ErrorBoundary
│   │   ├── pages/
│   │   │   ├── DashboardPage.tsx
│   │   │   ├── ProductsPage.tsx
│   │   │   ├── CategoriesSuppliersLocationsPage.tsx
│   │   │   ├── StockPage.tsx
│   │   │   ├── AlertsPage.tsx
│   │   │   └── ReportsPage.tsx
│   │   ├── types/
│   │   │   └── index.ts       # TypeScript interfaces matching API schemas
│   │   └── utils/
│   │       ├── formatters.ts  # currency, date, number
│   │       └── validators.ts  # client-side validation helpers
│   └── public/
└── _bmad-output/
    ├── PRD.md
    ├── planning-artifacts/
    └── implementation-artifacts/
```

---

## 8. Implementation Phases

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
- [ ] Verify assignment requirements met (checklist in Appendix)

---

## 9. Risks & Mitigations

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
| Hierarchical tree performance | Low | Low | Materialized `path` column; lazy-load children; virtualized list for 1000+ nodes |

---

## 10. Success Criteria

1. **Functional:** All Must-have user stories pass manual testing (CRUD + stock in/out/transfer + alerts + salesperson + reports)
2. **Database:** `flask db upgrade` creates schema cleanly on fresh `AIlearn` DB; migrations version-controlled in `migrations/versions/`
3. **API:** All 20+ endpoints respond correctly with JSON; validated via marshmallow schemas; consistent error format
4. **Frontend:** React app with 5 tabs + dashboard loads, performs all operations; TypeScript compiles without errors; TanStack Query caching works
5. **Documentation:** `schema.md` (Chinese), `README.md` (full setup), dbdiagram.io link; migration history in `migrations/versions/`
6. **Assignment Alignment:** Matches PPTX requirements (MVVM/MVC awareness, CRUD↔SQL↔HTTP, PostgreSQL, Flask, dbdiagram.io, React, Flask-Migrate)
7. **Educational Quality:** Code readable, commented, modular — suitable as teaching reference; demonstrates React + Flask + Flask-Migrate + TanStack Query best practices
8. **Testing:** `pytest` passes (unit + integration); `npm test` passes; test DB separate; CI-ready
9. **DevEx:** `flask seed-demo` works; `npm run dev` + `flask run` hot reload; `flask db` CLI functional; pre-commit hooks configured

---

## 11. Appendix: Assignment Checklist (from PPTX + Your Requirements + Research Enhancements)

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
| **Pre-commit 品質** | Best practice → ruff + eslint + pre-commit hooks |

---

*Generated using BMAD Method — Product Manager (John) perspective*  
*Next step: Run `bmad-architecture` to create technical architecture document, or `bmad-build` to start implementation.*