from flask import Blueprint

bp = Blueprint("api", __name__)

from . import courses, lessons, content, uploads, progress  # noqa: E402,F401
