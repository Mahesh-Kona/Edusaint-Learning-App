from flask import current_app
from ..models import Lesson
from ..extensions import cache
from . import bp


def cache_key(lesson_id, version):
    return f"lesson_content:{lesson_id}:v{version}"


@bp.route("/content/<int:lesson_id>", methods=["GET"])
def get_content(lesson_id):
    lesson = Lesson.query.filter_by(id=lesson_id).first_or_404()
    key = cache_key(lesson_id, lesson.content_version)
    cached = cache.get(key)
    if cached:
        # indicate cache hit (in logs)
        current_app.logger.debug(f"cache hit {key}")
        return {"success": True, "data": cached, "cached": True}
    payload = {"content_json": lesson.content_json, "schema_version": (lesson.content_json or {}).get("schema_version")}
    cache.set(key, payload)
    current_app.logger.debug(f"cache set {key}")
    return {"success": True, "data": payload, "cached": False}
