from flask import Blueprint, jsonify
from sqlalchemy import func

from app.models import Item
from app.extensions import db

dashboard_bp = Blueprint(
    "dashboard",
    __name__,
    url_prefix="/api/dashboard"
)
@dashboard_bp.route("", methods=["GET"])
def dashboard():
    total_items = db.session.query(func.count(Item.id)).scalar()
    total_stock = db.session.query(func.sum(Item.total_stock)).scalar() or 0
    total_used_stock = db.session.query(func.sum(Item.used_stock)).scalar() or 0

    return jsonify({
        "total_items": total_items,
        "total_stock": total_stock,
        "total_used_stock": total_used_stock
    }), 200