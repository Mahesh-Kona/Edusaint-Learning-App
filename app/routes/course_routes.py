# app/routes/course_routes.py
from flask import Blueprint, jsonify, request

course_bp = Blueprint('course', __name__)

# Test route
@course_bp.route('/test', methods=['GET'])
def test_course():
    return jsonify({"message": "Course routes working!"})

# Minimal GET courses endpoint placeholder
@course_bp.route('/', methods=['GET'])
def get_courses():
    page = request.args.get('page', 1)
    limit = request.args.get('limit', 10)
    # Placeholder data
    courses = [{"id": 1, "name": "Course 1"}, {"id": 2, "name": "Course 2"}]
    return jsonify({"page": page, "limit": limit, "courses": courses})
