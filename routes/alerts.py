"""
Alerts routes - low stock and reorder suggestions.
"""
from flask import Blueprint, request, jsonify
from models import db
from models.product import Product
from models.stock_item import StockItem
from models.supplier import Supplier
from models.product_supplier import ProductSupplier
from sqlalchemy import func

alerts_bp = Blueprint("alerts", __name__)


@alerts_bp.route("/alerts/low-stock", methods=["GET"])
def low_stock():
    """Real-time low stock alert."""
    include_zero = request.args.get("include_zero", "false").lower() == "true"

    query = Product.query.filter_by(is_active=True).filter(
        Product.available_stock <= Product.reorder_threshold
    )
    if not include_zero:
        query = query.filter(Product.available_stock > 0)

    products = query.order_by(Product.available_stock.asc()).all()

    return jsonify([{
        "id": p.id, "sku": p.sku, "name": p.name,
        "category": p.category.name if p.category else None,
        "current_stock": p.current_stock,
        "available_stock": p.available_stock,
        "reorder_threshold": p.reorder_threshold,
        "reorder_quantity": p.reorder_quantity,
        "unit_price": float(p.unit_price),
        "urgency_ratio": round(
            (p.reorder_threshold - p.available_stock) / p.reorder_threshold, 2
        ) if p.reorder_threshold > 0 else 0,
        "status": "OUT_OF_STOCK" if p.available_stock == 0 else "LOW_STOCK"
    } for p in products])


@alerts_bp.route("/alerts/reorder-suggestions", methods=["GET"])
def reorder_suggestions():
    """Suggested purchase orders grouped by supplier."""
    # Find low-stock products
    low_stock_products = Product.query.filter_by(is_active=True).filter(
        Product.available_stock <= Product.reorder_threshold
    ).all()

    if not low_stock_products:
        return jsonify([])

    # Group by preferred supplier
    supplier_groups = {}

    for product in low_stock_products:
        # Get preferred supplier link
        pref_link = ProductSupplier.query.filter_by(
            product_id=product.id, is_preferred=True
        ).first()

        if not pref_link:
            # Fallback to any supplier
            pref_link = ProductSupplier.query.filter_by(product_id=product.id).first()

        if not pref_link:
            continue

        supplier = Supplier.query.get(pref_link.supplier_id)
        if not supplier or not supplier.is_active:
            continue

        suggested_qty = product.reorder_quantity
        est_cost = float(pref_link.supplier_price or 0) * suggested_qty

        if supplier.id not in supplier_groups:
            supplier_groups[supplier.id] = {
                "supplier_id": supplier.id,
                "supplier_name": supplier.name,
                "supplier_email": supplier.email,
                "lead_time_days": supplier.lead_time_days,
                "items": [],
                "total_estimated_cost": 0
            }

        supplier_groups[supplier.id]["items"].append({
            "product_id": product.id,
            "sku": product.sku,
            "name": product.name,
            "current_stock": product.available_stock,
            "threshold": product.reorder_threshold,
            "suggested_qty": product.reorder_quantity,
            "supplier_sku": product.suppliers[0].supplier_sku if product.suppliers else None,
            "unit_cost": float(pref_link.supplier_price or 0),
            "estimated_cost": est_cost
        })
        supplier_groups[supplier.id]["total_estimated_cost"] += est_cost

    return jsonify(list(supplier_groups.values()))


@alerts_bp.route("/alerts/summary", methods=["GET"])
def alert_summary():
    """Quick summary for dashboard banner."""
    total_low = Product.query.filter_by(is_active=True).filter(
        Product.available_stock <= Product.reorder_threshold
    ).count()

    out_of_stock = Product.query.filter_by(is_active=True).filter(
        Product.available_stock == 0
    ).count()

    return jsonify({
        "low_stock_count": total_low,
        "out_of_stock_count": out_of_stock,
        "message": f"⚠️ {total_low} 項商品需補貨" if total_low > 0 else "✅ 庫存正常"
    })