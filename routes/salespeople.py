"""
Salesperson routes.
"""
from flask import Blueprint, request, jsonify
from models import db
from models.salesperson import Salesperson

salespeople_bp = Blueprint("salespeople", __name__)


@salespeople_bp.route("/salespeople", methods=["GET"])
def list_salespeople():
    page = request.args.get("page", 1, type=int)
    limit = min(request.args.get("limit", 20, type=int), 100)
    is_active = request.args.get("is_active", type=bool)

    query = Salesperson.query
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    query = query.order_by(Salesperson.name)
    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "items": [{
            "id": s.id, "name": s.name, "email": s.email,
            "phone": s.phone, "employee_id": s.employee_id,
            "hire_date": s.hire_date.isoformat() if s.hire_date else None,
            "is_active": s.is_active
        } for s in pagination.items],
        "total": pagination.total, "page": pagination.page,
        "pages": pagination.pages, "limit": limit
    })


@salespeople_bp.route("/salespeople", methods=["POST"])
def create_salesperson():
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"error": "VALIDATION_ERROR", "message": "Name required"}), 400

    sp = Salesperson(
        name=data["name"],
        email=data.get("email"),
        phone=data.get("phone"),
        employee_id=data.get("employee_id"),
        hire_date=data.get("hire_date"),
    )
    db.session.add(sp)
    db.session.commit()
    return jsonify({"id": sp.id, "message": "Salesperson created"}), 201


@salespeople_bp.route("/salespeople/<int:id>", methods=["GET"])
def get_salesperson(id):
    sp = Salesperson.query.get_or_404(id)
    return jsonify({
        "id": sp.id, "name": sp.name, "email": sp.email,
        "phone": sp.phone, "employee_id": sp.employee_id,
        "hire_date": sp.hire_date.isoformat() if sp.hire_date else None,
        "is_active": sp.is_active
    })


@salespeople_bp.route("/salespeople/<int:id>", methods=["PUT"])
def update_salesperson(id):
    sp = Salesperson.query.get_or_404(id)
    data = request.get_json()

    for field in ["name", "email", "phone", "employee_id", "hire_date", "is_active"]:
        if field in data:
            setattr(sp, field, data[field])

    db.session.commit()
    return jsonify({"message": "Salesperson updated"})


@salespeople_bp.route("/salespeople/<int:id>", methods=["DELETE"])
def delete_salesperson(id):
    sp = Salesperson.query.get_or_404(id)
    sp.is_active = False  # Soft delete
    db.session.commit()
    return "", 204