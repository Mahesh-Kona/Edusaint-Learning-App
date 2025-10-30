Migrations cleanup / squash instructions
=====================================

This repo contains historical Alembic migrations. For a clean production deploy you may want to squash them into a single baseline migration. Do NOT run this on a production DB without backups.

Safe approach (recommended):

1. Create a dump of your production DB and store it securely.
2. Spin up a fresh MySQL instance (empty DB).
3. In a branch, remove the `migrations/versions/` files (or move them to an archive folder) but keep `migrations/env.py` and `alembic.ini`.
4. Run:

   ```powershell
   set FLASK_APP=wsgi.py
   flask db stamp head
   flask db migrate -m "baseline"
   flask db upgrade
   ```

   This will create a single migration that represents the current models.

5. Verify schema in the fresh DB matches expectations. Compare with your dump if needed.
6. Merge the branch and deploy carefully. For existing production DBs you should NOT run the new baseline migration against a DB that already has the schema—use `flask db stamp head` to mark it as applied instead.

Alternative (non-destructive): keep history; create a maintenance plan and only perform squashing during a major migration window.
