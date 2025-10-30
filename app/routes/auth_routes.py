from flask import Blueprint, request, jsonify, current_app
from app.extensions import db, limiter
from app.models import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

auth_bp = Blueprint('auth_bp', __name__)


@auth_bp.route('/api/v1/auth/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    if not data.get('email') or not data.get('password'):
        return jsonify({"success": False, "error": "Email and password required", "code": 400}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"success": False, "error": "Email already registered", "code": 400}), 400

    new_user = User(email=data['email'], role=data.get('role', 'student'))
    new_user.set_password(data['password'])

    db.session.add(new_user)
    db.session.commit()

    # Return access + refresh tokens on registration
    # Use numeric identity and put role into additional claims to avoid subject-type issues
    # Use string identity for 'sub' to satisfy JWT libraries that expect a string
    access = create_access_token(identity=str(new_user.id), additional_claims={"role": new_user.role})
    refresh = create_refresh_token(identity=str(new_user.id), additional_claims={"role": new_user.role})
    return jsonify({"success": True, "message": "User registered successfully", "access_token": access, "refresh_token": refresh}), 201


@auth_bp.route('/api/v1/auth/login', methods=['POST'])
@limiter.limit("5/minute")
def login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=data.get('email')).first()

    if not user or not user.check_password(data.get('password')):
        return jsonify({"success": False, "error": "Invalid email or password", "code": 401}), 401

    access_token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
    refresh_token = create_refresh_token(identity=str(user.id), additional_claims={"role": user.role})
    return jsonify({
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {"id": user.id, "email": user.email, "role": user.role}
    }), 200



@auth_bp.route('/api/v1/auth/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    identity = get_jwt_identity()
    # issue a new access token
    access = create_access_token(identity=identity)
    return jsonify({"success": True, "access_token": access}), 200
