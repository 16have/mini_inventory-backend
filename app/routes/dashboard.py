from flask import Blueprint, jsonify
from sqlalchemy import func
from flask_jwt_extended import jwt_required

from app.models import Item
from app.extensions import db

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)

@jwt_required()
@dashboard_bp.route("", methods=["GET"])
def dashboard():

    total_item_types = db.session.query(func.count(Item.id)).scalar() or 0
    total_stock = db.session.query(func.sum(Item.total_stock)).scalar() or 0
    used_stock = db.session.query(func.sum(Item.used_stock)).scalar() or 0

    return jsonify({
        "total_item_types": total_item_types,
        "total_stock": total_stock,
        "used_stock": used_stock,
        "remaining_stock": total_stock - used_stock
    }), 200