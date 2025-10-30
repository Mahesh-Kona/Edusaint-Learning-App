from app.extensions import db
from app.models import User, Course, Lesson


def test_submit_progress(client):
    # create minimal user, course and lesson
    with client.application.app_context():
        u = User(email='p1@example.com')
        u.set_password('pass')
        db.session.add(u)
        c = Course(title='C1')
        db.session.add(c)
        db.session.commit()
        l = Lesson(course_id=c.id, title='L1')
        db.session.add(l)
        db.session.commit()
        user_id = u.id
        lesson_id = l.id

    payload = {"user_id": user_id, "lesson_id": lesson_id, "score": 0.85, "time_spent": 120, "answers": {"q1": "a"}}
    rv = client.post('/api/v1/progress', json=payload)
    assert rv.status_code == 200
    js = rv.get_json()
    assert js.get('success') is True
    assert 'id' in js
