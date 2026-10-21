"""
Dashboard routes - summary KPIs.
"""
from flask import Blueprint, request, jsonify
from models import db
from models.product import Product
from models.stock_movement import StockMovement
from models.salesperson import Salesperson
from sqlalchemy import func
from datetime import date, datetime, timedelta

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard/summary", methods=["GET"])
def dashboard_summary():
    """Dashboard KPIs."""
    today = date.today()
    week_ago = today - timedelta(days=7)

    # Total products
    total_products = Product.query.filter_by(is_active=True).count()

    # Low stock count
    low_stock_count = Product.query.filter_by(is_active=True).filter(
        Product.available_stock <= Product.reorder_threshold
    ).count()

    # Total stock value (current_stock * cost_price)
    total_stock_value = db.session.query(
        func.coalesce(func.sum(Product.current_stock * Product.cost_price), 0)
    ).filter(Product.is_active == True).scalar() or 0

    # Today's sales
    today_sales = db.session.query(
        func.coalesce(func.sum(StockMovement.total_amount), 0)
    ).filter(
        StockMovement.type == "out",
        StockMovement.reference_type == "sale",
        func.date(StockMovement.created_at) == today
    ).scalar() or 0

    # Today's transactions
    today_transactions = db.session.query(
        func.count(StockMovement.id)
    ).filter(
        StockMovement.type == "out",
        StockMovement.reference_type == "sale",
        func.date(StockMovement.created_at) == today
    ).scalar() or 0

    # This week's sales
    week_sales = db.session.query(
        func.coalesce(func.sum(StockMovement.total_amount), 0)
    ).filter(
        StockMovement.type == "out",
        StockMovement.reference_type == "sale",
        func.date(StockMovement.created_at) >= week_ago
    ).scalar() or 0

    # Top salespeople this week
    top_salespeople = db.session.query(
        Salesperson.id,
        Salesperson.name,
        func.coalesce(func.sum(StockMovement.total_amount), 0).label("revenue"),
        func.count(StockMovement.id).label("transactions")
    ).join(
        StockMovement,
        (StockMovement.salesperson_id == Salesperson.id) &
        (StockMovement.type == "out") &
        (StockMovement.reference_type == "sale")
    ).filter(
        Salesperson.is_active == True,
        func.date(StockMovement.created_at) >= week_ago
    ).group_by(Salesperson.id, Salesperson.name).order_by(
        func.sum(StockMovement.total_amount).desc()
    ).limit(5).all()

    return jsonify({
        "kpis": {
            "total_products": total_products,
            "low_stock_count": low_stock_count,
            "total_stock_value": round(float(total_stock_value), 2),
            "today_sales": round(float(today_sales), 2),
            "today_transactions": today_transactions,
            "week_sales": round(float(week_sales), 2)
        },
        "top_salespeople": [{
            "id": sp.id, "name": sp.name,
            "revenue": round(float(sp.revenue or 0), 2),
            "transactions": sp.transactions
        } for sp in top_salespeople]
    })