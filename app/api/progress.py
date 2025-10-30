from flask import request, current_app
from ..models import Progress
from ..extensions import db, limiter
from sqlalchemy.exc import IntegrityError
from . import bp


@bp.route("/progress", methods=["POST"])
@limiter.limit("30/minute")
def submit_progress():
    """Accept a progress submission. Prevent duplicate submissions when attempt_id is provided.

    Expected JSON: { user_id, lesson_id, score?, time_spent?, answers?, attempt_id? }
    """
    data = request.get_json(silent=True)
    if not data:
        return {"success": False, "error": "JSON payload required", "code": 400}, 400

    # Basic validation and type coercion
    try:
        user_id = int(data.get("user_id")) if data.get("user_id") is not None else None
    except Exception:
        return {"success": False, "error": "user_id must be integer", "code": 400}, 400
    try:
        lesson_id = int(data.get("lesson_id")) if data.get("lesson_id") is not None else None
    except Exception:
        return {"success": False, "error": "lesson_id must be integer", "code": 400}, 400

    if not (user_id and lesson_id):
        return {"success": False, "error": "user_id and lesson_id required", "code": 400}, 400

    attempt_id = data.get("attempt_id")
    score = data.get("score")
    time_spent = data.get("time_spent")
    answers = data.get("answers")

    # Prevent duplicate submission when attempt_id is provided
    if attempt_id:
        exists = Progress.query.filter_by(attempt_id=attempt_id, user_id=user_id, lesson_id=lesson_id).first()
        if exists:
            current_app.logger.info('Duplicate progress submission attempt_id=%s user_id=%s lesson_id=%s', attempt_id, user_id, lesson_id)
            return {"success": False, "error": "duplicate submission", "code": 409}, 409

    # Insert within a transaction
    p = Progress(user_id=user_id, lesson_id=lesson_id, score=score, time_spent=time_spent, answers=answers, attempt_id=attempt_id)
    try:
        with db.session.begin():
            db.session.add(p)
        return {"success": True, "id": p.id}
    except IntegrityError as e:
        # likely FK or constraint violation
        current_app.logger.exception('Progress insert IntegrityError')
        return {"success": False, "error": "db integrity error", "detail": str(e), "code": 500}, 500
    except Exception as e:
        current_app.logger.exception('Progress insert failed')
        return {"success": False, "error": "db error", "detail": str(e), "code": 500}, 500
