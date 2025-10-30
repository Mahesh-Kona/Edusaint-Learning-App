# Deliverables and how to run them

This file lists the deliverables requested and the exact places to find them in the repo, plus a short run-through to get everything running locally for React integration.

Files added / updated
- `Dockerfile` — builds the Flask app image (uses Gunicorn).
- `docker-compose.yml` — brings up `db` (MySQL 8), `redis`, and `web` (Flask). `uploads` is mounted as a named volume.
- `postman_collection.json` — Postman collection at repo root. Import into Postman to exercise auth, courses, lessons, content, uploads and progress.
- `docs/API.md`, `docs/DOCKER_FRONTEND.md`, `docs/POSTMAN.md`, `docs/RUN_THROUGH.md` — API docs and frontend run-through notes.
- `.github/workflows/ci.yml` — CI workflow to run migrations and tests on push/PR.
- `BACKLOG.md` — project backlog and next-sprint items.

Quick run-through (Docker)

1. Build and start services (MySQL and Redis + app):

```powershell
docker compose up --build -d
```

2. Initialize the DB schema (run migrations):

```powershell
# from host (requires flask & dependencies installed) or inside web container
docker compose exec web flask db upgrade
```

3. Verify app is running:

```powershell
curl http://localhost:5000/api/v1/courses
```

4. Import `postman_collection.json` into Postman and update the base URL if needed.

React dev integration

- Start Docker backend as above.
- Run React dev server locally (e.g. `npm start`) on `http://localhost:3000`.
- Ensure `CORS_ORIGINS` includes `http://localhost:3000` (set via `.env` or `docker-compose.yml`).
- From React, call `http://localhost:5000/api/v1/...` or configure a proxy in `package.json`.

If you'd like I can:
- Add a small `docker-compose.frontend.yml` that launches a basic static server for a built React app.
- Add a README badge pointing to the CI workflow (requires GitHub repo path).

Contact me which of those two you'd like next and I'll add it.
