"""Seed the database with demo data: users, course, lesson, progress.
Run with the project venv python, e.g.:
C:\...\venv\Scripts\python.exe scripts\seed_demo.py
"""
from app import create_app
from app.extensions import db
from app.models import User, Course, Lesson, Progress

app = create_app()

with app.app_context():
    # create any missing tables (safe for dev)
    db.create_all()

    # create users
    if not User.query.filter_by(email='student@example.com').first():
        u = User(email='student@example.com', role='student')
        u.set_password('StudentPass1')
        db.session.add(u)
        print('Created user student@example.com')
    if not User.query.filter_by(email='teacher@example.com').first():
        t = User(email='teacher@example.com', role='teacher')
        t.set_password('TeacherPass1')
        db.session.add(t)
        print('Created user teacher@example.com')

    db.session.commit()

    # create a course
    course = Course.query.filter_by(title='Demo Course').first()
    if not course:
        course = Course(title='Demo Course', description='Demo course for recording')
        db.session.add(course)
        db.session.commit()
        print('Created Demo Course id=', course.id)

    # create a lesson
    lesson = Lesson.query.filter_by(title='Intro Lesson', course_id=course.id).first()
    if not lesson:
        lesson = Lesson(
            course_id=course.id,
            title='Intro Lesson',
            content_json={'schema_version': 1, 'payload': {'blocks': []}},
            content_version=1,
        )
        db.session.add(lesson)
        db.session.commit()
        print('Created Intro Lesson id=', lesson.id)

    # create a progress row for student
    student = User.query.filter_by(email='student@example.com').first()
    if student and not Progress.query.filter_by(user_id=student.id, lesson_id=lesson.id).first():
        p = Progress(user_id=student.id, lesson_id=lesson.id, score=90.0, time_spent=120, answers={}, attempt_id='attempt-demo-1')
        db.session.add(p)
        db.session.commit()
        print('Created Progress id=', p.id)

    print('Seeding complete')
