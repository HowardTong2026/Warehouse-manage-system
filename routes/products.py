"""
Product routes - basic CRUD.
"""
from flask import Blueprint, request, jsonify
from models import db
from models.product import Product
from models.category import Category

products_bp = Blueprint("products", __name__)


@products_bp.route("/products", methods=["GET"])
def list_products():
    page = request.args.get("page", 1, type=int)
    limit = min(request.args.get("limit", 20, type=int), 100)
    search = request.args.get("search", "")
    category_id = request.args.get("category_id", type=int)
    low_stock = request.args.get("low_stock", type=bool)

    query = Product.query.filter_by(is_active=True)

    if search:
        query = query.filter(
            db.or_(
                Product.name.ilike(f"%{search}%"),
                Product.sku.ilike(f"%{search}%"),
                Product.barcode.ilike(f"%{search}%")
            )
        )
    if category_id:
        query = query.filter_by(category_id=category_id)
    if low_stock:
        query = query.filter(Product.available_stock <= Product.reorder_threshold)

    query = query.order_by(Product.name)
    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "items": [{
            "id": p.id, "name": p.name, "sku": p.sku, "barcode": p.barcode,
            "category_id": p.category_id, "category": p.category.name if p.category else None,
            "unit_price": float(p.unit_price), "cost_price": float(p.cost_price),
            "reorder_threshold": p.reorder_threshold, "reorder_quantity": p.reorder_quantity,
            "current_stock": p.current_stock, "available_stock": p.available_stock,
            "is_low_stock": p.is_low_stock
        } for p in pagination.items],
        "total": pagination.total,
        "page": pagination.page,
        "pages": pagination.pages,
        "limit": limit
    })


@products_bp.route("/products/<int:id>", methods=["GET"])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        "id": product.id, "name": product.name, "sku": product.sku,
        "barcode": product.barcode, "description": product.description,
        "category_id": product.category_id,
        "unit_price": float(product.unit_price), "cost_price": float(product.cost_price),
        "reorder_threshold": product.reorder_threshold,
        "reorder_quantity": product.reorder_quantity,
        "current_stock": product.current_stock, "available_stock": product.available_stock,
        "is_low_stock": product.is_low_stock
    })


@products_bp.route("/products", methods=["POST"])
def create_product():
    data = request.get_json()
    required = ["name", "sku", "unit_price"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": "VALIDATION_ERROR", "message": f"Missing required field: {field}"}), 400

    product = Product(
        name=data["name"],
        sku=data["sku"],
        barcode=data.get("barcode"),
        description=data.get("description"),
        category_id=data.get("category_id"),
        unit_price=data["unit_price"],
        cost_price=data.get("cost_price", 0),
        reorder_threshold=data.get("reorder_threshold", 10),
        reorder_quantity=data.get("reorder_quantity", 50),
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"id": product.id, "message": "Product created"}), 201


@products_bp.route("/products/<int:id>", methods=["PUT"])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()

    for field in ["name", "sku", "barcode", "description", "category_id",
                  "unit_price", "cost_price", "reorder_threshold", "reorder_quantity"]:
        if field in data:
            setattr(product, field, data[field])

    db.session.commit()
    return jsonify({"message": "Product updated"})


@products_bp.route("/products/<int:id>", methods=["DELETE"])
def delete_product(id):
    product = Product.query.get_or_404(id)
    product.is_active = False  # Soft delete
    db.session.commit()
    return "", 204