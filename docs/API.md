% API Reference — Flask Learning Backend

This document summarizes the main API endpoints implemented in this project and quick examples to exercise them.

Base URL (defaults)
- Local (development): http://127.0.0.1:5000
- Docker (when using docker-compose): http://localhost:5000

Authentication
- This API uses JWT access tokens (Flask-JWT-Extended). Obtain a token via login or register.

Endpoints (high level)

- POST /api/v1/auth/register
  - Request JSON: { email, password, role? }
  - Response: { success: true, access_token, refresh_token }

- POST /api/v1/auth/login
  - Request JSON: { email, password }
  - Response: { success: true, access_token, refresh_token, user }

- POST /api/v1/lessons
  - Protected: teacher/admin
  - Request JSON: { title, course_id, content_json }
  - Validates `content_json` against `app/schemas/lesson_schema.json`.

- PUT /api/v1/lessons/<id>
  - Protected: teacher/admin
  - Request JSON: { content_json }
  - On success increments `content_version`.

- GET /api/v1/content/<lesson_id>
  - Returns `content_json` and `schema_version` (cached by lesson_id + content_version).

- POST /api/v1/uploads
  - Accepts multipart/form-data file in key `file`.
  - Validates extension and size and saves to `UPLOAD_PATH` (local) or S3 (if configured).
  - Returns { success: true, url, size, mime_type, asset_created }

- POST /api/v1/progress
  - Accepts progress submissions: { user_id, lesson_id, score?, time_spent?, answers?, attempt_id? }
  - Prevents duplicate submissions when `attempt_id` is provided.

Debug / dev helpers
- GET /api/v1/debug/assets
  - Returns most recent uploaded assets (only when `DEBUG` or `ALLOW_DEBUG_ROUTES` is enabled in config).

Postman
- A Postman collection is included at `postman_collection.json`. Import it into Postman to run example requests and pre-configured auth.

Error format
- The API returns errors in a uniform JSON shape: { success: false, error: <message>, code: <http status> }

Notes
- JSON responses are configured with `JSON_AS_ASCII = False` to ensure utf8mb4-safe outputs.
- Pagination and query parameters exist for list endpoints (e.g., GET /api/v1/courses?page=&limit=).

If you need an OpenAPI/Swagger export, I can add a lightweight generator (Flask-apispec or flask-smorest) and produce a YAML/JSON spec.
