# Quick run-through for React integration

This short guide helps a frontend developer connect a React dev server to the running backend.

1) Start the backend
- Option A: Local (no Docker)
  - Activate your virtualenv and install requirements: `pip install -r requirements.txt`.
  - Set env var: `$env:FLASK_APP='wsgi.py'`
  - Run migrations: `flask db upgrade`
  - Start the app: `flask run` (or `python wsgi.py`)

- Option B: Docker (recommended for parity)
  - `docker compose up --build`
  - Migrate from inside the web container: `docker compose exec web flask db upgrade`

2) Start React dev server (frontend)
- In your React project `package.json` you can set the `proxy` to `http://localhost:5000` for simplified development, or make direct fetch calls to `http://localhost:5000/api/v1/...`.
- Example fetch URL: `fetch('http://localhost:5000/api/v1/content/1')`

3) CORS
- If the React dev app runs on port 3000, the compose file sets `CORS_ORIGINS` to `http://localhost:3000` by default. Change it in `.env` or `docker-compose.yml` if needed.

4) Uploads
- For local dev, `UPLOAD_PATH` is mounted from the repo `uploads` volume in docker-compose. When using the local Flask server (not Docker), ensure `UPLOAD_PATH` points to an existing directory and is writable by the process.

5) Testing
- Import `postman_collection.json` or use the `docs/API.md` to exercise endpoints.
