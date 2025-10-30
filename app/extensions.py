# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
# Rate limiter (init in create_app with app config)
# We'll create the Limiter here and pass storage_uri when initializing in create_app
limiter = Limiter(key_func=get_remote_address)
# Cache (SimpleCache by default, configurable via config)
cache = Cache()
