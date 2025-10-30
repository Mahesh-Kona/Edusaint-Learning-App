from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt


def require_roles(*roles):
    """
    Restrict access to users with specific roles.
    Usage: @require_roles("admin", "teacher")
    """
    def wrapper(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            verify_jwt_in_request()
            token = get_jwt()
            role = token.get("role")
            if not role or role not in roles:
                return jsonify({
                    "success": False,
                    "error": "Forbidden: Insufficient role",
                    "code": 403
                }), 403
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper
