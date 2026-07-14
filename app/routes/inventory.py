from flask import Blueprint, jsonify, request
from app.extensions import db
from app.models import Item
from flask_jwt_extended import jwt_required

inventory_bp = Blueprint(
    "inventory",
    __name__,
    url_prefix="/api/items"
)
@jwt_required()
@inventory_bp.route("", methods=["GET"])
def get_items():
    items = Item.query.all()

    return jsonify([item.to_dict() for item in items]), 200

@jwt_required()
@inventory_bp.route("/<int:item_id>", methods=["GET"])
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200

@jwt_required()
@inventory_bp.route("", methods=["POST"])
def create_item():
    data = request.get_json()

    if not data:
        return jsonify({"message": "Invalid JSON"}), 400

    name = data.get("name")
    description = data.get("description")
    total_stock = data.get("total_stock")
    user_id = data.get("user_id")

    if not name or total_stock is None or not user_id:
        return jsonify({"message": "Required fields are missing"}), 400

    if Item.find_by_name(name):
        return jsonify({"message": "Item already exists"}), 409

    item = Item(
        name=name,
        description=description,
        total_stock=total_stock,
        used_stock=0,
        user_id=user_id,
    )

    db.session.add(item)
    db.session.commit()

    return jsonify(item.to_dict()), 201

@jwt_required()
@inventory_bp.route("/<int:item_id>", methods=["PUT"])
def update_item(item_id):
    item = Item.query.get_or_404(item_id)

    data = request.get_json()

    item.name = data.get("name", item.name)
    item.description = data.get("description", item.description)
    item.total_stock = data.get("total_stock", item.total_stock)
    item.used_stock = data.get("used_stock", item.used_stock)

    db.session.commit()

    return jsonify(item.to_dict()), 200


@jwt_required()
@inventory_bp.route("/<int:item_id>", methods=["DELETE"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    db.session.delete(item)
    db.session.commit()

    return jsonify({
        "message": "Item deleted successfully"
    }), 200
