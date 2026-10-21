"""
Reports routes - salesperson performance, leaderboard.
"""
from flask import Blueprint, request, jsonify, make_response
from models import db
from models.salesperson import Salesperson
from models.stock_movement import StockMovement
from models.product import Product
from sqlalchemy import func, case
from datetime import datetime, date
import csv
import io

reports_bp = Blueprint("reports", __name__)


def _parse_date(d):
    if not d:
        return None
    try:
        return datetime.strptime(d, "%Y-%m-%d").date()
    except:
        return None


@reports_bp.route("/reports/salesperson/<int:sp_id>", methods=["GET"])
def salesperson_performance(sp_id):
    """Individual salesperson performance report."""
    from_date = _parse_date(request.args.get("from"))
    to_date = _parse_date(request.args.get("to"))
    group_by = request.args.get("group_by", "day")  # day, week, month

    sp = Salesperson.query.get_or_404(sp_id)

    query = StockMovement.query.filter(
        StockMovement.salesperson_id == sp_id,
        StockMovement.type == "out",
        StockMovement.reference_type == "sale"
    )

    if from_date:
        query = query.filter(StockMovement.created_at >= from_date)
    if to_date:
        query = query.filter(StockMovement.created_at <= to_date)

    movements = query.all()

    if not movements:
        return jsonify({
            "salesperson": {"id": sp.id, "name": sp.name, "employee_id": sp.employee_id},
            "period": {"from": str(from_date) if from_date else None, "to": str(to_date) if to_date else None},
            "summary": {"total_revenue": 0, "transaction_count": 0, "avg_order_value": 0},
            "top_products": [], "daily_breakdown": []
        })

    # Summary
    total_revenue = sum(float(m.total_amount or 0) for m in movements)
    transaction_count = len(movements)
    avg_order = total_revenue / transaction_count if transaction_count > 0 else 0

    # Top products
    product_stats = {}
    for m in movements:
        pid = m.product_id
        if pid not in product_stats:
            product_stats[pid] = {"qty": 0, "revenue": 0, "name": m.product.name}
        product_stats[pid]["qty"] += abs(m.quantity)
        product_stats[pid]["revenue"] += float(m.total_amount or 0)

    top_products = sorted(
        [{"product_id": pid, "name": v["name"], "qty_sold": v["qty"], "revenue": v["revenue"]}
         for pid, v in product_stats.items()],
        key=lambda x: x["revenue"], reverse=True
    )[:10]

    # Daily/weekly/monthly breakdown
    breakdown = {}
    for m in movements:
        dt = m.created_at.date()
        if group_by == "week":
            key = f"{dt.year}-W{dt.isocalendar()[1]:02d}"
        elif group_by == "month":
            key = f"{dt.year}-{dt.month:02d}"
        else:
            key = dt.isoformat()

        if key not in breakdown:
            breakdown[key] = {"revenue": 0, "transactions": 0}
        breakdown[key]["revenue"] += float(m.total_amount or 0)
        breakdown[key]["transactions"] += 1

    daily_breakdown = [
        {"period": k, "revenue": v["revenue"], "transactions": v["transactions"]}
        for k, v in sorted(breakdown.items())
    ]

    return jsonify({
        "salesperson": {"id": sp.id, "name": sp.name, "employee_id": sp.employee_id},
        "period": {"from": str(from_date) if from_date else None, "to": str(to_date) if to_date else None},
        "summary": {
            "total_revenue": round(total_revenue, 2),
            "transaction_count": transaction_count,
            "avg_order_value": round(avg_order, 2)
        },
        "top_products": top_products,
        "daily_breakdown": daily_breakdown
    })


@reports_bp.route("/reports/salespeople/leaderboard", methods=["GET"])
def leaderboard():
    """All salespeople ranked by revenue."""
    from_date = _parse_date(request.args.get("from"))
    to_date = _parse_date(request.args.get("to"))
    metric = request.args.get("metric", "revenue")  # revenue, transactions, avg_order

    query = db.session.query(
        Salesperson.id,
        Salesperson.name,
        Salesperson.employee_id,
        func.count(StockMovement.id).label("transactions"),
        func.coalesce(func.sum(StockMovement.total_amount), 0).label("total_revenue")
    ).join(
        StockMovement,
        (StockMovement.salesperson_id == Salesperson.id) &
        (StockMovement.type == "out") &
        (StockMovement.reference_type == "sale")
    ).filter(Salesperson.is_active == True).group_by(Salesperson.id, Salesperson.name, Salesperson.employee_id)

    if from_date:
        query = query.filter(StockMovement.created_at >= from_date)
    if to_date:
        query = query.filter(StockMovement.created_at <= to_date)

    results = query.all()

    if metric == "transactions":
        results = sorted(results, key=lambda x: x.transactions, reverse=True)
    elif metric == "avg_order":
        results = sorted(results, key=lambda x: (x.total_revenue / x.transactions) if x.transactions > 0 else 0, reverse=True)
    else:
        results = sorted(results, key=lambda x: x.total_revenue, reverse=True)

    return jsonify([{
        "rank": i + 1,
        "salesperson_id": r.id,
        "name": r.name,
        "employee_id": r.employee_id,
        "total_revenue": round(float(r.total_revenue), 2),
        "transaction_count": r.transactions,
        "avg_order_value": round(float(r.total_revenue) / r.transactions, 2) if r.transactions > 0 else 0
    } for i, r in enumerate(results)])


@reports_bp.route("/reports/salesperson/<int:sp_id>/export", methods=["GET"])
def export_salesperson(sp_id):
    """Export salesperson performance as CSV."""
    from_date = _parse_date(request.args.get("from"))
    to_date = _parse_date(request.args.get("to"))

    sp = Salesperson.query.get_or_404(sp_id)

    query = StockMovement.query.filter(
        StockMovement.salesperson_id == sp_id,
        StockMovement.type == "out",
        StockMovement.reference_type == "sale"
    )
    if from_date:
        query = query.filter(StockMovement.created_at >= from_date)
    if to_date:
        query = query.filter(StockMovement.created_at <= to_date)

    movements = query.order_by(StockMovement.created_at).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Date", "Product", "SKU", "Quantity", "Unit Price", "Total", "Reference ID", "Reason"])

    for m in movements:
        writer.writerow([
            m.created_at.date().isoformat(),
            m.product.name if m.product else "N/A",
            m.product.sku if m.product else "N/A",
            abs(m.quantity),
            float(m.unit_price_at_time),
            float(m.total_amount or 0),
            m.reference_id or "",
            m.reason or ""
        ])

    response = make_response(output.getvalue())
    response.headers["Content-Type"] = "text/csv"
    response.headers["Content-Disposition"] = f"attachment; filename=salesperson_{sp_id}_report.csv"
    return response