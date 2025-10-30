<#
Runs the repository's CI steps locally. Requires Docker and PowerShell.

What it does:
- Starts services via docker-compose (MySQL + Redis)
- Waits for MySQL to be ready
- Installs Python deps in the active environment
- Runs migrations and pytest

Usage: Open PowerShell at repo root and run:
  .\scripts\run_ci_locally.ps1

#>

Write-Host "Starting docker-compose services..." -ForegroundColor Cyan
docker-compose up -d --build

# Wait for MySQL
Write-Host "Waiting for MySQL to accept connections..." -ForegroundColor Cyan
$max = 60
for ($i=0; $i -lt $max; $i++) {
    try {
        & mysqladmin ping -h 127.0.0.1 -P 3306 -u root -ppassword > $null 2>&1
        if ($LASTEXITCODE -eq 0) { Write-Host "MySQL is ready"; break }
    } catch {
    }
    Start-Sleep -Seconds 2
}

Write-Host "Installing Python dependencies (local env)..." -ForegroundColor Cyan
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Running migrations..." -ForegroundColor Cyan
$env:FLASK_APP = 'wsgi.py'
flask db upgrade

Write-Host "Running tests..." -ForegroundColor Cyan
pytest -q

Write-Host "Done. If you want to stop containers run: docker-compose down" -ForegroundColor Green
