"""
Supplier routes.
"""
from flask import Blueprint, request, jsonify
from models import db
from models.supplier import Supplier

suppliers_bp = Blueprint("suppliers", __name__)


@suppliers_bp.route("/suppliers", methods=["GET"])
def list_suppliers():
    page = request.args.get("page", 1, type=int)
    limit = min(request.args.get("limit", 20, type=int), 100)
    is_active = request.args.get("is_active", type=bool)

    query = Supplier.query
    if is_active is not None:
        query = query.filter_by(is_active=is_active)
    query = query.order_by(Supplier.name)
    pagination = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "items": [{
            "id": s.id, "name": s.name, "contact_name": s.contact_name,
            "email": s.email, "phone": s.phone, "address": s.address,
            "lead_time_days": s.lead_time_days, "is_active": s.is_active
        } for s in pagination.items],
        "total": pagination.total, "page": pagination.page,
        "pages": pagination.pages, "limit": limit
    })


@suppliers_bp.route("/suppliers", methods=["POST"])
def create_supplier():
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"error": "VALIDATION_ERROR", "message": "Name required"}), 400

    sup = Supplier(
        name=data["name"],
        contact_name=data.get("contact_name"),
        email=data.get("email"),
        phone=data.get("phone"),
        address=data.get("address"),
        lead_time_days=data.get("lead_time_days", 7),
    )
    db.session.add(sup)
    db.session.commit()
    return jsonify({"id": sup.id, "message": "Supplier created"}), 201


@suppliers_bp.route("/suppliers/<int:id>", methods=["PUT"])
def update_supplier(id):
    sup = Supplier.query.get_or_404(id)
    data = request.get_json()

    for field in ["name", "contact_name", "email", "phone", "address", "lead_time_days", "is_active"]:
        if field in data:
            setattr(sup, field, data[field])

    db.session.commit()
    return jsonify({"message": "Supplier updated"})


@suppliers_bp.route("/suppliers/<int:id>", methods=["DELETE"])
def delete_supplier(id):
    sup = Supplier.query.get_or_404(id)
    sup.is_active = False
    db.session.commit()
    return "", 204