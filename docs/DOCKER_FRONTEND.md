# Docker + Frontend integration notes

This project provides a backend Flask service and a docker-compose configuration that starts MySQL and Redis along with the Flask app.

docker-compose behavior
- `docker-compose.yml` (root) defines services:
  - `db`: MySQL 8.0 (character set utf8mb4)
  - `redis`: Redis for caching and rate-limiting
  - `web`: the Flask application (built from the repository `Dockerfile`)

Running locally with Docker

1. Build and start services:

```powershell
docker compose up --build
```

2. After the MySQL container is ready, run migrations from a shell (or from a container):

```powershell
# from the running web container:
docker compose exec web flask db upgrade
```

Frontend (React) integration

There is no frontend source included in this repo. Typical integration steps for a React dev server:

1. Start the Flask backend (docker compose up).
2. Start your React dev server locally (e.g., `npm start`) on port 3000.
3. Ensure the backend allows CORS from the React dev host. The compose file sets `CORS_ORIGINS` to `http://localhost:3000` by default; you can override via `.env` or the compose file.
4. In the React app, point API requests at `http://localhost:5000/api/v1/...` and upload to `http://localhost:5000/api/v1/uploads`.

Proxying option

If you prefer to proxy API requests via the React dev server, add a `proxy` entry to `package.json` (only for dev) or configure the dev server to proxy `/api` to `http://localhost:5000`.

Serving a production frontend

If you build a static React app (`npm run build`) you can add a `frontend` service to `docker-compose.yml` that uses a static server (nginx or `serve`) to host the built files and configure the `CORS_ORIGINS` accordingly.

Notes
- The compose file mounts `uploads` as a named volume so uploaded files persist between restarts.
- If you change `UPLOAD_PATH` in the environment, make sure the `web` service has a matching volume mount.
