with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Update UI/UX section
old_uiux = """## 6. UI/UX Specification

### 6.1 Single-Page Layout (Tabs for Teaching Clarity)
| Tab | Section | Components |
|-----|---------|------------|
| **📦 產品管理** | Header | Title: "Inventory Management" |
| | Toolbar | "Add Product" button (opens modal) |
| | Main Table | Columns: SKU, Name, Category, Price, Stock, Threshold, **Status**, Actions |
| | Status Badge | Green "OK" / **Red "LOW STOCK — 需補貨"** (current_stock ≤ threshold) |
| | Add/Edit Modal | Form with all product fields |
| **📥 進貨/銷貨** | Stock In Modal | Product dropdown, quantity, reason |
| | Stock Out Modal | Product dropdown, quantity, reason, **Salesperson dropdown (required)** |
| | Movement Log | Table: Date, Product, Type, Qty, Price, Salesperson, Reason |
| **🔔 補貨提醒** | Alert Banner | **Sticky top bar: "⚠️ X 項商品需補貨" — click to filter** |
| | Low-Stock Table | Only products ≤ threshold; sortable by urgency (stock/threshold ratio) |
| **👥 業績報表** | Salesperson Selector | Dropdown to pick salesperson + date range picker |
| | KPI Cards | Total Revenue, Transactions, Avg Order Value |
| | Top Products Table | Product, Qty Sold, Revenue |
| | Daily Chart | Simple bar chart (JS) or table: Date, Revenue, Transactions |
| | Leaderboard Table | Rank, Salesperson, Revenue, Transactions |

### 6.2 Interaction Flow
1. Page loads → `GET /api/products` → render **產品管理** table
2. **補貨提醒** tab auto-loads `GET /api/alerts/low-stock` → render low-stock table
3. Click "Stock Out" on row → modal → **must select salesperson** → submit → `POST /api/stock/out` → refresh row + update alerts
4. **業績報表** tab → select salesperson + date range → `GET /api/reports/salesperson/:id` → render KPIs + charts
5. Leaderboard button → `GET /api/reports/salespeople/leaderboard` → render ranked table"""

new_uiux = """## 6. UI/UX Specification

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
| Role-based visibility | flask-react-inventory | Admin sees cost/margin; Staff sees only own transactions |"""

if old_uiux in content:
    content = content.replace(old_uiux, new_uiux)
    print("UI/UX updated!")
else:
    print("UI/UX NOT FOUND - trying regex")
    import re
    pattern = r'## 6\. UI/UX Specification[\s\S]*?---\n'
    new_content, count = re.subn(pattern, new_uiux + '\n\n---\n', content, flags=re.MULTILINE)
    if count > 0:
        content = new_content
        print("UI/UX updated via regex!")
    else:
        print("UI/UX regex also failed")

with open(r'C:\Users\user\Desktop\AI學習第八課\_bmad-output\PRD.md', 'w', encoding='utf-8') as f:
    f.write(content)