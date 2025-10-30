from . import bp
from ..models import Lesson


@bp.route("/lessons/<int:id>", methods=["GET"])
def get_lesson(id):
    l = Lesson.query.with_entities(Lesson.id, Lesson.title, Lesson.course_id, Lesson.content_version, Lesson.created_at).filter_by(id=id).first_or_404()
    return {"success": True, "data": {"id": l.id, "title": l.title, "course_id": l.course_id, "content_version": l.content_version, "created_at": l.created_at.isoformat()}}
