import json
import sys, os
# ensure project root is on sys.path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import create_app
from app.extensions import db


def test_courses_list(client=None):
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_ENGINE_OPTIONS": {},
    })
    with app.app_context():
        db.create_all()
        # create a course via direct model to keep test simple
        from app.models import Course
        c = Course(title="Test Course", description="desc")
        db.session.add(c)
        db.session.commit()
        client = app.test_client()
        rv = client.get('/api/v1/courses')
        assert rv.status_code == 200
        data = rv.get_json()
        assert data['success'] is True
        assert isinstance(data['data'], list)
        assert any(item['title'] == 'Test Course' for item in data['data'])
        db.session.remove()
        db.drop_all()
