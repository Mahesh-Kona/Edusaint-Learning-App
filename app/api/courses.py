from flask import request, jsonify, current_app
from ..models import Course, Lesson
from ..extensions import db
from . import bp


@bp.route("/courses", methods=["GET"])
def list_courses():
    # pagination
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 20))
    except ValueError:
        page, limit = 1, 20

    q = Course.query
    # filters (title)
    title = request.args.get("title")
    if title:
        q = q.filter(Course.title.ilike(f"%{title}%"))

    # select only required columns (optimization)
    q = q.with_entities(Course.id, Course.title, Course.description, Course.created_at)

    items = q.order_by(Course.created_at.desc()).paginate(page=page, per_page=limit, error_out=False)
    data = [{"id": c.id, "title": c.title, "description": c.description, "created_at": c.created_at.isoformat()} for c in items.items]
    return {"success": True, "data": data, "meta": {"page": items.page, "pages": items.pages, "total": items.total}}

@bp.route("/courses/<int:id>", methods=["GET"])
def get_course(id):
    c = Course.query.with_entities(Course.id, Course.title, Course.description, Course.created_at).filter_by(id=id).first_or_404()
    return {"success": True, "data": {"id": c.id, "title": c.title, "description": c.description, "created_at": c.created_at.isoformat()}}

@bp.route("/courses/<int:id>/lessons", methods=["GET"])
def get_course_lessons(id):
    # only select minimized fields
    lessons = Lesson.query.with_entities(Lesson.id, Lesson.title, Lesson.content_version, Lesson.created_at).filter_by(course_id=id).order_by(Lesson.created_at.asc()).all()
    data = [{"id": l.id, "title": l.title, "content_version": l.content_version, "created_at": l.created_at.isoformat()} for l in lessons]
    return {"success": True, "data": data}
