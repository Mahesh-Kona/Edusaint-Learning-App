from flask import Blueprint, request, current_app
from jsonschema import validate, ValidationError
from ..models import Lesson
from ..extensions import db
from ..decorators import require_roles
from flask_jwt_extended import jwt_required
import json, os

from . import bp

# load schema
schema_path = os.path.join(os.path.dirname(__file__), "..", "schemas", "lesson_schema.json")
with open(schema_path, "r") as fh:
    lesson_schema = json.load(fh)

@bp.route("/lessons", methods=["POST"])
@jwt_required()
@require_roles("teacher", "admin")
def create_lesson():
    data = request.get_json() or {}
    title = data.get("title")
    course_id = data.get("course_id")
    content_json = data.get("content_json")
    if not title or not course_id or content_json is None:
        return {"success": False, "error": "missing fields", "code": 400}, 400
    try:
        validate(instance=content_json, schema=lesson_schema)
    except ValidationError as e:
        return {"success": False, "error": f"invalid content_json: {e.message}", "code": 400}, 400
    lesson = Lesson(title=title, course_id=course_id, content_json=content_json, content_version=1)
    db.session.add(lesson); db.session.commit()
    return {"success": True, "id": lesson.id}

@bp.route("/lessons/<int:id>", methods=["PUT"])
@jwt_required()
@require_roles("teacher", "admin")
def update_lesson(id):
    lesson = Lesson.query.get_or_404(id)
    data = request.get_json() or {}
    content_json = data.get("content_json")
    if content_json is None:
        return {"success": False, "error": "content_json required", "code": 400}, 400
    try:
        validate(instance=content_json, schema=lesson_schema)
    except ValidationError as e:
        return {"success": False, "error": f"invalid content_json: {e.message}", "code": 400}, 400
    lesson.content_json = content_json
    lesson.content_version = (lesson.content_version or 1) + 1
    db.session.commit()
    return {"success": True, "id": lesson.id, "content_version": lesson.content_version}
