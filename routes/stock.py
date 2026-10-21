"""
Stock movement routes - stock in, out, transfer.
"""
from flask import Blueprint, request, jsonify
from models import db
from models.product import Product
from models.location import Location
from models.stock_item import StockItem
from models.stock_movement import StockMovement
from models.salesperson import Salesperson
from models.supplier import Supplier
from sqlalchemy import func

stock_bp = Blueprint("stock", __name__)


def _get_or_create_stock_item(product_id, location_id, batch_number=None):
    """Get or create stock item for product at location."""
    stock_item = StockItem.query.filter_by(
        product_id=product_id, location_id=location_id
    ).first()
    if not stock_item:
        stock_item = StockItem(
            product_id=product_id,
            location_id=location_id,
            quantity=0, reserved=0, available=0
        )
        db.session.add(stock_item)
        db.session.flush()
    return stock_item


@stock_bp.route("/stock/in", methods=["POST"])
def stock_in():
    """Receive stock (purchase)."""
    data = request.get_json()
    required = ["product_id", "location_id", "quantity", "unit_price"]
    for field in required:
        if field not in data:
            return jsonify({"error": "VALIDATION_ERROR", "message": f"Missing {field}"}), 400

    product = Product.query.get_or_404(data["product_id"])
    location = Location.query.get_or_404(data["location_id"])
    quantity = data["quantity"]
    unit_price = data["unit_price"]

    if quantity <= 0:
        return jsonify({"error": "VALIDATION_ERROR", "message": "Quantity must be positive"}), 400

    # Create stock item if needed
    stock_item = _get_or_create_stock_item(data["product_id"], data["location_id"])
    stock_item.quantity += quantity
    stock_item.compute_available()

    # Create movement record
    movement = StockMovement(
        product_id=data["product_id"],
        location_id=data["location_id"],
        type="in",
        reference_type="purchase",
        reference_id=data.get("reference_id"),
        quantity=quantity,
        unit_price_at_time=data["unit_price"],
        total_amount=data["unit_price"] * quantity,
        reason=data.get("reason", "Stock received"),
        supplier_id=data.get("supplier_id"),
        changed_by=data.get("changed_by", "system"),
    )
    db.session.add(movement)

    # Update product totals
    product = Product.query.get(data["product_id"])
    product.current_stock += quantity
    product.compute_available_stock()

    db.session.commit()

    return jsonify({
        "message": "Stock received",
        "movement_id": movement.id,
        "product_id": data["product_id"],
        "new_stock": Product.query.get(data["product_id"]).current_stock
    }), 201


@stock_bp.route("/stock/out", methods=["POST"])
def stock_out():
    """Record sale (stock-out with salesperson)."""
    data = request.get_json()
    required = ["product_id", "location_id", "quantity", "unit_price", "salesperson_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": "VALIDATION_ERROR", "message": f"Missing {field}"}), 400

    product = Product.query.get_or_404(data["product_id"])
    location = Location.query.get_or_404(data["location_id"])
    salesperson = Salesperson.query.get_or_404(data["salesperson_id"])
    quantity = data["quantity"]
    unit_price = data["unit_price"]

    if quantity <= 0:
        return jsonify({"error": "VALIDATION_ERROR", "message": "Quantity must be positive"}), 400

    # Check available stock
    stock_item = StockItem.query.filter_by(
        product_id=data["product_id"], location_id=data["location_id"]
    ).first()
    available = stock_item.available if stock_item else 0

    if available < data["quantity"]:
        return jsonify({
            "error": "CONFLICT",
            "message": f"Insufficient stock. Available: {available}, Requested: {data['quantity']}"
        }), 400

    # Validate salesperson
    if not salesperson.is_active:
        return jsonify({"error": "VALIDATION_ERROR", "message": "Salesperson not active"}), 400

    # Update stock item
    stock_item = StockItem.query.filter_by(
        product_id=data["product_id"], location_id=data["location_id"]
    ).first()
    stock_item.quantity -= data["quantity"]
    stock_item.compute_available()

    # Create movement record
    quantity = data["quantity"]
    movement = StockMovement(
        product_id=data["product_id"],
        location_id=data["location_id"],
        salesperson_id=data["salesperson_id"],
        type="out",
        reference_type="sale",
        reference_id=data.get("reference_id"),
        quantity=-quantity,
        unit_price_at_time=data["unit_price"],
        total_amount=data["unit_price"] * quantity,
        reason=data.get("reason", "Sale"),
        changed_by=data.get("changed_by", "system"),
    )
    db.session.add(movement)

    # Update product totals
    product = Product.query.get(data["product_id"])
    product.current_stock -= quantity
    product.compute_available_stock()

    # Update stock item
    stock_item = StockItem.query.filter_by(
        product_id=data["product_id"], location_id=data["location_id"]
    ).first()
    stock_item.quantity -= quantity
    stock_item.compute_available()

    db.session.commit()

    return jsonify({
        "message": "Sale recorded",
        "movement_id": StockMovement.query.order_by(StockMovement.id.desc()).first().id,
        "product_id": data["product_id"],
        "new_stock": Product.query.get(data["product_id"]).current_stock,
        "salesperson_name": Salesperson.query.get(data["salesperson_id"]).name
    }), 201


@stock_bp.route("/stock/transfer", methods=["POST"])
def stock_transfer():
    """Transfer stock between locations."""
    data = request.get_json()
    required = ["product_id", "from_location_id", "to_location_id", "quantity"]
    for field in required:
        if field not in data:
            return jsonify({"error": "VALIDATION_ERROR", "message": f"Missing {field}"}), 400

    product = Product.query.get_or_404(data["product_id"])
    from_loc = Location.query.get_or_404(data["from_location_id"])
    to_loc = Location.query.get_or_404(data["to_location_id"])
    quantity = data["quantity"]

    if quantity <= 0:
        return jsonify({"error": "VALIDATION_ERROR", "message": "Quantity must be positive"}), 400

    # Check source stock
    from_stock = StockItem.query.filter_by(
        product_id=data["product_id"], location_id=data["from_location_id"]
    ).first()
    if not from_stock or from_stock.available < quantity:
        avail = from_stock.available if from_stock else 0
        return jsonify({
            "error": "CONFLICT",
            "message": f"Insufficient stock at source. Available: {avail}"
        }), 400

    # Out from source
    out_movement = StockMovement(
        product_id=data["product_id"],
        location_id=data["from_location_id"],
        type="out",
        reference_type="transfer",
        reference_id=data.get("reference_id"),
        quantity=-data["quantity"],
        unit_price_at_time=product.cost_price,
        total_amount=product.cost_price * data["quantity"],
        reason=data.get("reason", f"Transfer to {Location.query.get(data['to_location_id']).name}"),
        changed_by=data.get("changed_by", "system"),
    )
    db.session.add(out_movement)

    from_stock = StockItem.query.filter_by(
        product_id=data["product_id"], location_id=data["from_location_id"]
    ).first()
    from_stock.quantity -= quantity
    from_stock.compute_available()

    # In to destination
    to_stock = StockItem.query.filter_by(
        product_id=data["product_id"], location_id=data["to_location_id"]
    ).first()
    if not to_stock:
        to_stock = StockItem(
            product_id=data["product_id"],
            location_id=data["to_location_id"],
            quantity=0, reserved=0, available=0
        )
        db.session.add(to_stock)
        db.session.flush()

    in_movement = StockMovement(
        product_id=data["product_id"],
        location_id=data["to_location_id"],
        type="in",
        reference_type="transfer",
        reference_id=data.get("reference_id"),
        quantity=data["quantity"],
        unit_price_at_time=product.cost_price,
        total_amount=product.cost_price * data["quantity"],
        reason=data.get("reason", f"Transfer from {Location.query.get(data['from_location_id']).name}"),
        changed_by=data.get("changed_by", "system"),
    )
    db.session.add(in_movement)

    to_stock.quantity += quantity
    to_stock.compute_available()

    db.session.commit()

    return jsonify({
        "message": "Transfer completed",
        "out_movement_id": out_movement.id,
        "in_movement_id": in_movement.id
    }), 201


@stock_bp.route("/products/<int:product_id>/movements", methods=["GET"])
def get_movements(product_id):
    page = request.args.get("page", 1, type=int)
    limit = min(request.args.get("limit", 20, type=int), 100)
    movement_type = request.args.get("type")
    from_date = request.args.get("from")
    to_date = request.args.get("to")

    Product.query.get_or_404(product_id)

    query = StockMovement.query.filter_by(product_id=product_id).order_by(StockMovement.created_at.desc())

    if movement_type:
        query = query.filter_by(type=movement_type)
    if from_date:
        query = query.filter(StockMovement.created_at >= from_date)
    if to_date:
        query = query.filter(StockMovement.created_at <= to_date)

    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "items": [{
            "id": m.id, "type": m.type, "reference_type": m.reference_type,
            "quantity": m.quantity, "unit_price_at_time": float(m.unit_price_at_time),
            "total_amount": float(m.total_amount) if m.total_amount else None,
            "reason": m.reason, "salesperson": m.salesperson.name if m.salesperson else None,
            "supplier": m.supplier.name if m.supplier else None,
            "location": m.location.name if m.location else None,
            "created_at": m.created_at.isoformat()
        } for m in pagination.items],
        "total": pagination.total, "page": pagination.page,
        "pages": pagination.pages, "limit": limit
    })