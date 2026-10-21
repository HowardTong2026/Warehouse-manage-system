"""
Location routes.
"""
from flask import Blueprint, request, jsonify
from models import db
from models.location import Location

locations_bp = Blueprint("locations", __name__)


@locations_bp.route("/locations", methods=["GET"])
def list_locations():
    tree = request.args.get("tree", "false").lower() == "true"
    query = Location.query.filter_by(is_active=True).order_by(Location.path, Location.name)

    if tree:
        locations = query.all()
        return jsonify(_build_tree(locations))
    else:
        locations = query.all()
        return jsonify([{
            "id": l.id, "name": l.name, "description": l.description,
            "parent_id": l.parent_id, "path": l.path, "level": l.level,
            "full_path": l.get_full_path()
        } for l in locations])


def _build_tree(locations):
    loc_map = {l.id: {"id": l.id, "name": l.name, "description": l.description,
                       "parent_id": l.parent_id, "path": l.path, "level": l.level,
                       "full_path": l.get_full_path(), "children": []} for l in locations}
    roots = []
    for loc in loc_map.values():
        if loc["parent_id"] and loc["parent_id"] in loc_map:
            loc_map[loc["parent_id"]]["children"].append(loc)
        else:
            roots.append(loc)
    return roots


@locations_bp.route("/locations", methods=["POST"])
def create_location():
    from models import db
    data = request.get_json()
    if not data.get("name"):
        return jsonify({"error": "VALIDATION_ERROR", "message": "Name required"}), 400

    loc = Location(
        name=data["name"],
        description=data.get("description"),
        parent_id=data.get("parent_id"),
    )
    db.session.add(loc)
    db.session.flush()
    loc.update_path()
    db.session.commit()
    return jsonify({"id": loc.id, "message": "Location created"}), 201


@locations_bp.route("/locations/<int:id>", methods=["PUT"])
def update_location(id):
    from models import db
    loc = Location.query.get_or_404(id)
    data = request.get_json()

    for field in ["name", "description", "parent_id"]:
        if field in data:
            setattr(loc, field, data[field])

    loc.update_path()
    db.session.commit()
    return jsonify({"message": "Location updated"})


@locations_bp.route("/locations/<int:id>", methods=["DELETE"])
def delete_location(id):
    from models import db
    loc = Location.query.get_or_404(id)
    loc.is_active = False
    db.session.commit()
    return "", 204