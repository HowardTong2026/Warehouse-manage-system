"""
Category routes.
"""
from flask import Blueprint, request, jsonify
from models import db
from models.category import Category

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/categories", methods=["GET"])
def list_categories():
    tree = request.args.get("tree", "false").lower() == "true"
    query = Category.query.filter_by(is_active=True).order_by(Category.path, Category.name)

    if tree:
        categories = query.all()
        return jsonify(_build_tree(categories))
    else:
        categories = query.all()
        return jsonify([{
            "id": c.id, "name": c.name, "description": c.description,
            "parent_id": c.parent_id, "path": c.path, "level": c.level,
            "full_path": c.get_full_path()
        } for c in categories])


def _build_tree(categories):
    """Build nested tree from flat list."""
    cat_map = {c.id: {"id": c.id, "name": c.name, "description": c.description,
                       "parent_id": c.parent_id, "path": c.path, "level": c.level,
                       "full_path": c.get_full_path(), "children": []} for c in categories}
    roots = []
    for cat in cat_map.values():
        if cat["parent_id"] and cat["parent_id"] in cat_map:
            cat_map[cat["parent_id"]]["children"].append(cat)
        else:
            roots.append(cat)
    return roots


@categories_bp.route("/categories", methods=["POST"])
def create_category():
    from models import db
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"error": "VALIDATION_ERROR", "message": "Name required"}), 400

    cat = Category(
        name=data["name"],
        description=data.get("description"),
        parent_id=data.get("parent_id"),
    )
    db.session.add(cat)
    db.session.flush()
    cat.update_path()
    db.session.commit()
    return jsonify({"id": cat.id, "message": "Category created"}), 201


@categories_bp.route("/categories/<int:id>", methods=["PUT"])
def update_category(id):
    from models import db
    cat = Category.query.get_or_404(id)
    data = request.get_json()

    for field in ["name", "description", "parent_id"]:
        if field in data:
            setattr(cat, field, data[field])

    cat.update_path()
    db.session.commit()
    return jsonify({"message": "Category updated"})


@categories_bp.route("/categories/<int:id>", methods=["DELETE"])
def delete_category(id):
    from models import db
    cat = Category.query.get_or_404(id)
    cat.is_active = False
    db.session.commit()
    return "", 204