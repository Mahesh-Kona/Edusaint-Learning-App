from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_all_errors(e):
        if isinstance(e, HTTPException):
            code = e.code
            message = getattr(e, "description", str(e))
        else:
            code = 500
            message = str(e)
        response = {"success": False, "error": message, "code": code}
        return jsonify(response), code
