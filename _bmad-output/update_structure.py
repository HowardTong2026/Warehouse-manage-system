with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Update Project Structure section
old_structure = """## 7. Project Structure

```
AI學習第八課/
├── .env                      # DB credentials (gitignored)
├── .flaskenv                 # FLASK_APP, FLASK_ENV
├── config.py                 # Configuration (環境變數管理)
├── app.py                    # Flask app factory (create_app)
├── models/                   # SQLAlchemy models (Flask-Migrate 管理)
│   ├── __init__.py           # db = SQLAlchemy()
│   ├── category.py
│   ├── product.py
│   ├── salesperson.py
│   └── stock_movement.py
├── migrations/               # Flask-Migrate 產生的遷移腳本 (git tracked)
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
├── services/                 # 業務邏輯層 (可單元測試)
│   ├── __init__.py
│   ├── product_service.py
│   ├── stock_service.py
│   ├── alert_service.py
│   ├── salesperson_service.py
│   └── report_service.py
├── routes/                   # REST API 路由 (Blueprint)
│   ├── __init__.py
│   ├── products.py
│   ├── stock.py
│   ├── alerts.py
│   ├── salespeople.py
│   └── reports.py
├── schemas/                  # 請求/響應驗證 (marshmallow 或 pydantic)
│   ├── __init__.py
│   ├── product_schema.py
│   ├── stock_schema.py
│   └── report_schema.py
├── frontend/                 # React + Vite + TypeScript
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── index.html
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx
│   │   ├── api/
│   │   │   ├── client.ts      # Axios instance with baseURL
│   │   │   └── endpoints.ts   # API endpoint constants
│   │   ├── hooks/
│   │   │   ├── useProducts.ts
│   │   │   ├── useStock.ts
│   │   │   ├── useSalespeople.ts
│   │   │   └── useReports.ts
│   │   ├── components/
│   │   │   ├── layout/
│   │   │   ├── products/
│   │   │   ├── stock/
│   │   │   ├── alerts/
│   │   │   ├── reports/
│   │   │   └── ui/
│   │   ├── pages/
│   │   │   ├── ProductsPage.tsx
│   │   │   ├── StockPage.tsx
│   │   │   ├── AlertsPage.tsx
│   │   │   └── ReportsPage.tsx
│   │   ├── types/
│   │   │   └── index.ts       # TypeScript interfaces matching API
│   │   └── utils/
│   └── public/
└── _bmad-output/
    ├── PRD.md
    ├── planning-artifacts/
    └── implementation-artifacts/
```"""

new_structure = """## 7. Project Structure

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
```"""

if old_structure in content:
    content = content.replace(old_structure, new_structure)
    print("Project Structure updated!")
else:
    print("Project Structure NOT FOUND")

with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'w', encoding='utf-8') as f:
    f.write(content)