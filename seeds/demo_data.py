"""
Demo data seeding for teaching purposes.
Run with: flask seed-demo --password <password>
"""
from datetime import date, datetime
from decimal import Decimal
from models import db
from models.category import Category
from models.supplier import Supplier
from models.product import Product
from models.product_supplier import ProductSupplier
from models.location import Location
from models.stock_item import StockItem
from models.salesperson import Salesperson
from models.stock_movement import StockMovement


def create_demo_data(password: str = "demo123"):
    """Create comprehensive demo data for teaching."""
    print("Creating demo data...")

    # Clear existing data (in reverse dependency order)
    StockMovement.query.delete()
    StockItem.query.delete()
    ProductSupplier.query.delete()
    Product.query.delete()
    Location.query.delete()
    Category.query.delete()
    Supplier.query.delete()
    Salesperson.query.delete()
    db.session.commit()

    # ==========================================
    # 1. Categories (hierarchical)
    # ==========================================
    cat_electronics = Category(name="Electronics", description="Electronic devices and components", parent_id=None)
    cat_computers = Category(name="Computers", description="Computing devices", parent_id=None)
    cat_accessories = Category(name="Accessories", description="Computer accessories", parent_id=None)
    cat_components = Category(name="Components", description="Electronic components", parent_id=None)
    cat_office = Category(name="Office Supplies", description="Office and stationery", parent_id=None)
    cat_furniture = Category(name="Furniture", description="Office furniture", parent_id=None)

    db.session.add_all([
        cat_electronics, cat_computers, cat_accessories,
        cat_components, cat_office, cat_furniture
    ])
    db.session.flush()

    # Set parent relationships
    cat_laptops = Category(name="Laptops", description="Portable computers", parent_id=cat_computers.id)
    cat_desktops = Category(name="Desktops", description="Desktop computers", parent_id=cat_computers.id)
    cat_monitors = Category(name="Monitors", description="Display monitors", parent_id=cat_accessories.id)
    cat_keyboards = Category(name="Keyboards", description="Input devices", parent_id=cat_accessories.id)
    cat_resistors = Category(name="Resistors", description="Passive components", parent_id=cat_components.id)
    cat_capacitors = Category(name="Capacitors", description="Passive components", parent_id=cat_components.id)
    cat_paper = Category(name="Paper", description="Printing paper", parent_id=cat_office.id)
    cat_pens = Category(name="Pens", description="Writing instruments", parent_id=cat_office.id)
    cat_chairs = Category(name="Chairs", description="Office chairs", parent_id=cat_furniture.id)
    cat_desks = Category(name="Desks", description="Office desks", parent_id=cat_furniture.id)

    db.session.add_all([
        cat_laptops, cat_desktops, cat_monitors, cat_keyboards,
        cat_resistors, cat_capacitors, cat_paper, cat_pens, cat_chairs, cat_desks
    ])
    db.session.flush()

    # Update paths
    for cat in Category.query.all():
        cat.update_path()
    db.session.commit()

    # ==========================================
    # 2. Suppliers
    # ==========================================
    sup_techcorp = Supplier(
        name="TechCorp International",
        contact_name="John Chen",
        email="sales@techcorp.com",
        phone="+1-555-0101",
        address="123 Tech Park, Silicon Valley, CA 94000",
        lead_time_days=5
    )
    sup_global = Supplier(
        name="Global Components Ltd",
        contact_name="Maria Santos",
        email="orders@globalcomp.com",
        phone="+1-555-0202",
        address="456 Industrial Blvd, Shenzhen, China",
        lead_time_days=14
    )
    sup_officeplus = Supplier(
        name="OfficePlus Wholesale",
        contact_name="David Kim",
        email="b2b@officeplus.com",
        phone="+1-555-0303",
        address="789 Business Ave, Dallas, TX 75000",
        lead_time_days=3
    )
    sup_furniture = Supplier(
        name="ErgoFurniture Co",
        contact_name="Lisa Wang",
        email="sales@ergofurniture.com",
        phone="+1-555-0404",
        address="321 Design District, Portland, OR 97200",
        lead_time_days=10
    )

    db.session.add_all([sup_techcorp, sup_global, sup_officeplus, sup_furniture])
    db.session.flush()

    # ==========================================
    # 3. Locations (hierarchical warehouse)
    # ==========================================
    loc_warehouse_a = Location(name="Warehouse A", description="Main warehouse", parent_id=None)
    loc_warehouse_b = Location(name="Warehouse B", description="Secondary warehouse", parent_id=None)

    db.session.add_all([loc_warehouse_a, loc_warehouse_b])
    db.session.flush()

    loc_zone_1 = Location(name="Zone 1 - Electronics", parent_id=loc_warehouse_a.id)
    loc_zone_2 = Location(name="Zone 2 - Office", parent_id=loc_warehouse_a.id)
    loc_zone_3 = Location(name="Zone 3 - Furniture", parent_id=loc_warehouse_a.id)
    loc_receiving = Location(name="Receiving Dock", parent_id=loc_warehouse_b.id)
    loc_shipping = Location(name="Shipping Area", parent_id=loc_warehouse_b.id)

    db.session.add_all([loc_zone_1, loc_zone_2, loc_zone_3, loc_receiving, loc_shipping])
    db.session.flush()

    for loc in Location.query.all():
        loc.update_path()
    db.session.commit()

    # ==========================================
    # 4. Salespeople
    # ==========================================
    sp_alice = Salesperson(
        name="Alice Chen",
        email="alice.chen@company.com",
        phone="+1-555-1001",
        employee_id="EMP001",
        hire_date=date(2022, 3, 15)
    )
    sp_bob = Salesperson(
        name="Bob Martinez",
        email="bob.martinez@company.com",
        phone="+1-555-1002",
        employee_id="EMP002",
        hire_date=date(2022, 6, 20)
    )
    sp_carol = Salesperson(
        name="Carol Lee",
        email="carol.lee@company.com",
        phone="+1-555-1003",
        employee_id="EMP003",
        hire_date=date(2023, 1, 10)
    )
    sp_david = Salesperson(
        name="David Park",
        email="david.park@company.com",
        phone="+1-555-1004",
        employee_id="EMP004",
        hire_date=date(2023, 4, 5)
    )

    db.session.add_all([sp_alice, sp_bob, sp_carol, sp_david])
    db.session.flush()

    # ==========================================
    # 5. Products with supplier links
    # ==========================================
    products_data = [
        # (name, sku, barcode, description, category, unit_price, cost_price,
        #  reorder_threshold, reorder_qty, suppliers: [(supplier, supplier_sku, supplier_price, is_preferred)])
        ("MacBook Pro 14\" M3", "MBP14-M3-512", "0194253210123",
         "Apple MacBook Pro 14-inch with M3 chip, 512GB SSD",
         cat_laptops, 1999.00, 1650.00, 5, 10,
         [(sup_techcorp, "MBP14M3-512", 1600.00, True)]),

        ("MacBook Pro 16\" M3 Max", "MBP16-M3MAX-1TB", "0194253210124",
         "Apple MacBook Pro 16-inch with M3 Max, 1TB SSD",
         cat_laptops, 3499.00, 2800.00, 3, 5,
         [(sup_techcorp, "MBP16M3M-1TB", 2750.00, True)]),

        ("Dell XPS 15", "DELL-XPS15-512", "0884116352147",
         "Dell XPS 15 with Intel i7, 512GB SSD",
         cat_laptops, 1599.00, 1200.00, 5, 10,
         [(sup_global, "DXPS15-512", 1150.00, True),
          (sup_techcorp, "DXPS15-512", 1180.00, False)]),

        ("Dell UltraSharp 27\" 4K", "DELL-U27-4K", "0884116352148",
         "27-inch 4K USB-C Monitor",
         cat_monitors, 499.00, 350.00, 8, 15,
         [(sup_global, "DU27-4K", 330.00, True)]),

        ("Logitech MX Master 3S", "LOGI-MX3S", "097855165432",
         "Wireless Performance Mouse",
         cat_accessories, 99.00, 60.00, 15, 30,
         [(sup_global, "LMX3S", 55.00, True)]),

        ("Keychron K8 Pro", "KEY-K8PRO", "6950370321456",
         "Wireless Mechanical Keyboard, 80%",
         cat_keyboards, 129.00, 80.00, 10, 20,
         [(sup_global, "K8PRO", 75.00, True)]),

        ("10kΩ Resistor 1/4W 1%", "RES-10K-1%", "6950370321457",
         "Through-hole 10k Ohm 1/4 Watt 1% Resistor (pack of 100)",
         cat_resistors, 4.99, 2.00, 50, 200,
         [(sup_global, "R-10K-1%", 1.50, True)]),

        ("100µF Electrolytic Cap", "CAP-100UF-25V", "6950370321458",
         "Radial 100uF 25V Electrolytic Capacitor (pack of 50)",
         cat_capacitors, 8.99, 4.00, 30, 100,
         [(sup_global, "C-100U-25V", 3.50, True)]),

        ("A4 Copy Paper 500 sheets", "PAPER-A4-500", "6950370321459",
         "Premium A4 80gsm Copy Paper",
         cat_paper, 5.99, 3.50, 20, 50,
         [(sup_officeplus, "A4-80G-500", 3.00, True)]),

        ("Pilot G2 Gel Pen 0.7mm", "PEN-G2-07", "6950370321460",
         "Retractable Gel Pen, Blue Ink (pack of 12)",
         cat_pens, 12.99, 6.00, 15, 40,
         [(sup_officeplus, "G2-07-BLUE", 5.50, True)]),

        ("Herman Miller Aeron", "HMAERON-B", "6950370321461",
         "Ergonomic Office Chair, Size B, Graphite",
         cat_chairs, 1395.00, 900.00, 2, 5,
         [(sup_furniture, "AERON-B-GRPH", 850.00, True)]),

        ("Uplift V2 Standing Desk", "UPLIFT-V2-72", "6950370321462",
         "72\" Standing Desk, Bamboo Top",
         cat_desks, 899.00, 550.00, 3, 8,
         [(sup_furniture, "V2-72-BMB", 520.00, True)]),
    ]

    products = []
    for data in products_data:
        (name, sku, barcode, description, category, unit_price, cost_price,
         reorder_threshold, reorder_qty, supplier_links) = data

        prod = Product(
            name=name,
            sku=sku,
            barcode=barcode,
            description=description,
            category_id=category.id,
            unit_price=Decimal(str(unit_price)),
            cost_price=Decimal(str(cost_price)),
            reorder_threshold=reorder_threshold,
            reorder_quantity=reorder_qty,
            current_stock=0,  # Will be set via stock items
            reserved_stock=0,
            available_stock=0,
        )
        db.session.add(prod)
        products.append((prod, supplier_links))

    db.session.flush()

    # Create ProductSupplier links
    for prod, supplier_links in products:
        for sup, sup_sku, sup_price, is_pref in supplier_links:
            ps = ProductSupplier(
                product_id=prod.id,
                supplier_id=sup.id,
                supplier_sku=sup_sku,
                supplier_price=Decimal(str(sup_price)),
                is_preferred=is_pref,
            )
            db.session.add(ps)

    db.session.commit()

    # ==========================================
    # 6. Stock Items (per-location inventory)
    # ==========================================
    stock_data = [
        # (product_sku, location_name, qty, batch)
        ("MBP14-M3-512", "Zone 1 - Electronics", 15, "BATCH-2024-001"),
        ("MBP16-M3MAX-1TB", "Zone 1 - Electronics", 5, "BATCH-2024-002"),
        ("DELL-XPS15-512", "Zone 1 - Electronics", 20, "BATCH-2024-003"),
        ("DELL-U27-4K", "Zone 1 - Electronics", 25, "BATCH-2024-004"),
        ("LOGI-MX3S", "Zone 2 - Office", 50, "BATCH-2024-005"),
        ("KEY-K8PRO", "Zone 2 - Office", 30, "BATCH-2024-006"),
        ("RES-10K-1%", "Zone 1 - Electronics", 500, "BATCH-2024-007"),
        ("CAP-100UF-25V", "Zone 1 - Electronics", 200, "BATCH-2024-008"),
        ("PAPER-A4-500", "Zone 2 - Office", 100, "BATCH-2024-009"),
        ("PEN-G2-07", "Zone 2 - Office", 80, "BATCH-2024-010"),
        ("HMAERON-B", "Zone 3 - Furniture", 8, "BATCH-2024-011"),
        ("UPLIFT-V2-72", "Zone 3 - Furniture", 12, "BATCH-2024-012"),
    ]

    # Create stock items and initial stock movements (stock-in)
    for sku, loc_name, qty, batch in stock_data:
        prod = Product.query.filter_by(sku=sku).first()
        loc = Location.query.filter_by(name=loc_name).first()

        if prod and loc:
            # Create stock item
            stock_item = StockItem(
                product_id=prod.id,
                location_id=loc.id,
                quantity=qty,
                reserved=0,
                available=qty,
                batch_number=batch,
            )
            db.session.add(stock_item)

            # Create initial stock-in movement
            movement = StockMovement(
                product_id=prod.id,
                location_id=loc.id,
                type="in",
                reference_type="purchase",
                quantity=qty,
                unit_price_at_time=prod.cost_price,
                total_amount=prod.cost_price * qty,
                reason=f"Initial stock - {batch}",
                changed_by="system",
            )
            db.session.add(movement)

            # Update product denormalized totals
            prod.current_stock += qty
            prod.available_stock += qty

    db.session.commit()

    # ==========================================
    # 7. Sample Stock Movements (sales, adjustments)
    # ==========================================
    # Get some products and salespeople for sample movements
    mbp14 = Product.query.filter_by(sku="MBP14-M3-512").first()
    dell_xps = Product.query.filter_by(sku="DELL-XPS15-512").first()
    dell_mon = Product.query.filter_by(sku="DELL-U27-4K").first()
    logi_mouse = Product.query.filter_by(sku="LOGI-MX3S").first()
    keychron = Product.query.filter_by(sku="KEY-K8PRO").first()
    paper = Product.query.filter_by(sku="PAPER-A4-500").first()
    pen = Product.query.filter_by(sku="PEN-G2-07").first()
    chair = Product.query.filter_by(sku="HMAERON-B").first()
    desk = Product.query.filter_by(sku="UPLIFT-V2-72").first()

    loc_z1 = Location.query.filter_by(name="Zone 1 - Electronics").first()
    loc_z2 = Location.query.filter_by(name="Zone 2 - Office").first()
    loc_z3 = Location.query.filter_by(name="Zone 3 - Furniture").first()

    sales_data = [
        # (product, salesperson, qty, unit_price, reference_type, reference_id, reason)
        (mbp14, sp_alice, 2, Decimal("1999.00"), "sale", 1001, "Customer order #1001"),
        (dell_xps, sp_bob, 1, Decimal("1599.00"), "sale", 1002, "Customer order #1002"),
        (dell_mon, sp_carol, 3, Decimal("499.00"), "sale", 1003, "Customer order #1003"),
        (logi_mouse, sp_alice, 5, Decimal("99.00"), "sale", 1004, "Customer order #1004"),
        (keychron, sp_david, 2, Decimal("129.00"), "sale", 1005, "Customer order #1005"),
        (paper, sp_bob, 10, Decimal("5.99"), "sale", 1006, "Customer order #1006"),
        (pen, sp_carol, 12, Decimal("12.99"), "sale", 1007, "Customer order #1007"),
        (chair, sp_david, 1, Decimal("1395.00"), "sale", 1008, "Customer order #1008"),
        (desk, sp_alice, 1, Decimal("899.00"), "sale", 1009, "Customer order #1009"),
    ]

    for prod, salesperson, qty, unit_price, ref_type, ref_id, reason in sales_data:
        if not prod or not salesperson:
            continue

        # Create stock-out movement
        movement = StockMovement(
            product_id=prod.id,
            location_id=loc_z1.id if prod.category_id in [cat_laptops.id, cat_desktops.id, cat_monitors.id, cat_keyboards.id, cat_resistors.id, cat_capacitors.id] else (
                loc_z2.id if prod.category_id in [cat_keyboards.id, cat_paper.id, cat_pens.id] else loc_z3.id
            ),
            salesperson_id=salesperson.id,
            type="out",
            reference_type=ref_type,
            reference_id=ref_id,
            quantity=-qty,
            unit_price_at_time=unit_price,
            total_amount=unit_price * qty,
            reason=reason,
            changed_by=salesperson.name,
        )
        db.session.add(movement)

        # Update product stock
        prod.current_stock -= qty
        prod.compute_available_stock()

        # Update stock item
        stock_item = StockItem.query.filter_by(
            product_id=prod.id,
            location_id=movement.location_id
        ).first()
        if stock_item:
            stock_item.quantity -= qty
            stock_item.compute_available()

    # Add some adjustments
    adj_data = [
        (logi_mouse, "adjustment", -2, "Damaged during handling", sp_alice),
        (paper, "adjustment", 5, "Found misplaced stock", sp_bob),
    ]

    for prod, adj_type, qty, reason, sp in adj_data:
        if not prod:
            continue
        movement = StockMovement(
            product_id=prod.id,
            location_id=loc_z2.id,
            salesperson_id=sp.id if sp else None,
            type=adj_type,
            reference_type="adjustment",
            quantity=qty,
            unit_price_at_time=prod.cost_price,
            total_amount=prod.cost_price * abs(qty),
            reason=reason,
            changed_by=sp.name if sp else "system",
        )
        db.session.add(movement)
        prod.current_stock += qty
        prod.compute_available_stock()

        stock_item = StockItem.query.filter_by(
            product_id=prod.id,
            location_id=loc_z2.id
        ).first()
        if stock_item:
            stock_item.quantity += qty
            stock_item.compute_available()

    db.session.commit()

    # Final sync of available_stock for all products
    for prod in Product.query.all():
        prod.compute_available_stock()
    db.session.commit()

    print("[OK] Demo data created successfully!")
    print(f"   Categories: {Category.query.count()}")
    print(f"   Suppliers: {Supplier.query.count()}")
    print(f"   Products: {Product.query.count()}")
    print(f"   Locations: {Location.query.count()}")
    print(f"   Stock Items: {StockItem.query.count()}")
    print(f"   Salespeople: {Salesperson.query.count()}")
    print(f"   Stock Movements: {StockMovement.query.count()}")