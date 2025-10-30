from app.extensions import db
from app.models import Course, Lesson


def test_content_cache_flag(client):
    # create course and lesson with content
    with client.application.app_context():
        c = Course(title='CacheCourse')
        db.session.add(c)
        db.session.commit()
        l = Lesson(course_id=c.id, title='CachedLesson', content_json={"schema_version": 1, "data": {"k": "v"}})
        db.session.add(l)
        db.session.commit()
        lid = l.id

    # first request should set cache
    r1 = client.get(f'/api/v1/content/{lid}')
    assert r1.status_code == 200
    j1 = r1.get_json()
    assert j1['success'] is True
    assert j1['cached'] is False

    # second request should be cached
    r2 = client.get(f'/api/v1/content/{lid}')
    assert r2.status_code == 200
    j2 = r2.get_json()
    assert j2['success'] is True
    assert j2['cached'] is True
