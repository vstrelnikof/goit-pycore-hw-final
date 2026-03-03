# Встановлення Git-хуків (pre-commit + pre-push) з оновленням ревізій.
# Запускати з кореня проєкту, з активованим venv:
#   .\scripts\setup-hooks.ps1

$ErrorActionPreference = "Stop"

Write-Host "pre-commit autoupdate..." -ForegroundColor Cyan
pre-commit autoupdate

Write-Host "pre-commit install (pre-commit + pre-push)..." -ForegroundColor Cyan
pre-commit install
pre-commit install --hook-type pre-push

Write-Host "Done. Run: pre-commit run --all-files" -ForegroundColor Green
