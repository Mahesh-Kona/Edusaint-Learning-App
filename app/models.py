from datetime import datetime
from sqlalchemy.dialects.mysql import JSON as MySQLJSON
from sqlalchemy import Index
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# Column for JSON detection: fallback to Text if MySQL < 5.7 is used is left to SQLA dialect.
JSON_COL = MySQLJSON

class User(db.Model):  # type: ignore[name-defined]
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum("student","teacher","admin", name="user_roles"), default="student", nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Course(db.Model):  # type: ignore[name-defined]
    __tablename__ = "courses"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), index=True, nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Lesson(db.Model):  # type: ignore[name-defined]
    __tablename__ = "lessons"
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), index=True, nullable=False)
    title = db.Column(db.String(255), nullable=False, index=True)
    content_json = db.Column(JSON_COL, nullable=True)
    content_version = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    course = db.relationship("Course", backref=db.backref("lessons", lazy="dynamic"))

class Topic(db.Model):  # type: ignore[name-defined]
    __tablename__ = "topics"
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), index=True, nullable=False)
    title = db.Column(db.String(255))
    data_json = db.Column(JSON_COL)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

class Asset(db.Model):  # type: ignore[name-defined]
    __tablename__ = "assets"
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(1024), nullable=False)
    # allow nullable uploader_id so anonymous uploads can be recorded
    uploader_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=True)
    size = db.Column(db.Integer)
    mime_type = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    uploader = db.relationship("User")

class Progress(db.Model):  # type: ignore[name-defined]
    __tablename__ = "progress"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), index=True, nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lessons.id"), index=True, nullable=False)
    score = db.Column(db.Float)
    time_spent = db.Column(db.Integer)  # seconds
    answers = db.Column(JSON_COL)
    attempt_id = db.Column(db.String(255), nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    user = db.relationship("User")
    lesson = db.relationship("Lesson")

# Index examples (if you want explicit composite indexes)
Index("ix_progress_user_lesson", Progress.user_id, Progress.lesson_id)
