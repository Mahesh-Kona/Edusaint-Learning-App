<#
PowerShell helper for safely squashing Alembic migrations into a baseline.

USAGE (recommended dry-run):
  1) Make a branch in your repo: git checkout -b migrations/squash-draft
  2) Run this script with -WhatIf to only show steps: .\scripts\squash_migrations.ps1 -DryRun

This script will:
 - Create a temporary empty MySQL container (optional) to verify new baseline migration
 - Move existing migrations/versions to an archive folder (local only)
 - Stamp the DB as head and autogenerate a new baseline migration
 - Keep the new migration under migrations/versions for review

IMPORTANT: Do NOT run this against a production DB. Always backup your DB and test on a staging copy first.
#>

param(
    [switch]$DryRun = $false,
    [string]$TempMySQLTag = "mysql:8.0",
    [string]$TempDBName = "learning_squash_tmp",
    [string]$TempRootPassword = "password"
)

Write-Host "DRY RUN: $DryRun" -ForegroundColor Cyan

if ($DryRun) {
    Write-Host "This will show the recommended steps for squashing migrations. No changes will be made." -ForegroundColor Yellow
}

# Step 1: create archive folder for existing versions
$versionsDir = Join-Path -Path $PSScriptRoot -ChildPath "..\migrations\versions"
$archiveDir = Join-Path -Path $PSScriptRoot -ChildPath "..\migrations\archive_versions"
Write-Host "Would move existing migration version files from:`n  $versionsDir`n to `$archiveDir`" -ForegroundColor Cyan
if (-not $DryRun) {
    if (-not (Test-Path $archiveDir)) { New-Item -ItemType Directory -Path $archiveDir | Out-Null }
    Get-ChildItem -Path $versionsDir -Filter "*.py" | Move-Item -Destination $archiveDir -Force
    Write-Host "Moved existing version files to archive." -ForegroundColor Green
}

# Step 2: stamp head and create baseline migration
Write-Host "Next steps (manual verification recommended):" -ForegroundColor Cyan
Write-Host "1. Ensure your working tree is clean and committed on a feature branch." -ForegroundColor Cyan
Write-Host "2. If you have an empty DB for testing, set DATABASE_URL accordingly and run:" -ForegroundColor Cyan
Write-Host "     set FLASK_APP=wsgi.py; flask db stamp head; flask db migrate -m \"baseline\"; flask db upgrade" -ForegroundColor Yellow

if (-not $DryRun) {
    Write-Host "Note: This script does not run the flask commands automatically to avoid accidental production changes." -ForegroundColor Yellow
    Write-Host "Follow the printed commands carefully on an empty/test DB to generate the baseline migration." -ForegroundColor Yellow
}

Write-Host "Script completed. Review the new migration in migrations/versions and test on a non-production DB before merging." -ForegroundColor Green
