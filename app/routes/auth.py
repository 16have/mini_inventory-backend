from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app.extensions import db
from app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    if User.find_by_email(email):
        return jsonify({"message": "Email already exists"}), 409

    if User.find_by_username(username):
        return jsonify({"message": "Username already exists"}), 409

    password_hash = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.find_by_email(email)

    if user is None:
        return jsonify({"message": "Invalid credentials"}), 401

    if not check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid credentials"}), 401
    
    token = create_access_token(
    identity=user.id
    )
    
    return jsonify({

    "access_token": token,

    "user": user.to_dict()

}),200

    