# app/routes/lesson_routes.py
from flask import Blueprint, jsonify, request

lesson_bp = Blueprint('lesson', __name__)

# Test route
@lesson_bp.route('/test', methods=['GET'])
def test_lesson():
    return jsonify({"message": "Lesson routes working!"})

# Minimal GET lesson by id placeholder
@lesson_bp.route('/<int:lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    # Placeholder data
    lesson = {"id": lesson_id, "title": f"Lesson {lesson_id}", "content": "Lesson content placeholder"}
    return jsonify(lesson)
