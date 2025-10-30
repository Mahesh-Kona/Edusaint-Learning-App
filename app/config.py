import os
from datetime import timedelta
from urllib.parse import quote_plus
from dotenv import load_dotenv

# Load .env file if present (development convenience)
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=int(os.getenv("JWT_ACCESS_MINUTES", "15")))
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=int(os.getenv("JWT_REFRESH_DAYS", "7")))

    # SQLAlchemy
    DATABASE_URL = os.getenv("DATABASE_URL", None)
    if not DATABASE_URL:
        user = os.getenv("MYSQL_USER", "root")
        pw = quote_plus(os.getenv("MYSQL_PASSWORD", "password"))
        host = os.getenv("MYSQL_HOST", "db")
        port = os.getenv("MYSQL_PORT", "3306")
        db = os.getenv("MYSQL_DATABASE", "learning")
        # ensure utf8mb4 charset and proper args
        DATABASE_URL = f"mysql+pymysql://{user}:{pw}@{host}:{port}/{db}?charset=utf8mb4"

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Pool & recycle (avoid stale connections)
    # For SQLite in-memory testing we avoid passing pool args that are invalid for StaticPool
    if DATABASE_URL.startswith('sqlite'):
        SQLALCHEMY_ENGINE_OPTIONS = {}
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_size": int(os.getenv("POOL_SIZE", 10)),
            "max_overflow": int(os.getenv("MAX_OVERFLOW", 20)),
            "pool_recycle": int(os.getenv("POOL_RECYCLE", 1800)),  # seconds
            "pool_pre_ping": True
        }

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")  # set to your React origin(s) in production

    # Uploads
    UPLOAD_PATH = os.getenv("UPLOAD_PATH", "/tmp/uploads")
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # 16 MB

    # Caching
    CACHE_TYPE = os.getenv("CACHE_TYPE", "SimpleCache")  # "RedisCache" if using redis
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", 300))

    # Redis / cache settings (used when CACHE_TYPE=RedisCache)
    REDIS_URL = os.getenv("REDIS_URL", os.getenv("CACHE_REDIS_URL", None))
    if REDIS_URL:
        CACHE_TYPE = os.getenv("CACHE_TYPE", "RedisCache")
        CACHE_REDIS_URL = REDIS_URL

    # Rate limiter storage (Flask-Limiter)
    RATELIMIT_STORAGE_URL = os.getenv("RATELIMIT_STORAGE_URL", REDIS_URL)

    # Rate limiting
    RATELIMIT_HEADERS_ENABLED = True
    # Default rate limits (comma-separated, can be overridden per route)
    RATELIMIT_DEFAULTS = os.getenv('RATELIMIT_DEFAULTS', '200 per day;50 per hour')

    # Content Security Policy (basic default, override in production)
    CONTENT_SECURITY_POLICY = os.getenv('CONTENT_SECURITY_POLICY', "default-src 'self'; img-src 'self' data: https:; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';")

    # Ensure Flask JSON responses do not escape unicode (keep utf8 characters like emoji)
    JSON_AS_ASCII = False
