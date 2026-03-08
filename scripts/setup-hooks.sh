#!/usr/bin/env bash
# Встановлення Git-хуків (pre-commit + pre-push) з оновленням ревізій.
# Запускати з кореня проєкту, з активованим venv:
#   bash scripts/setup-hooks.sh

set -e

echo "pre-commit autoupdate..."
pre-commit autoupdate

echo "pre-commit install (pre-commit + pre-push)..."
pre-commit install
pre-commit install --hook-type pre-push

echo "Done. Run: pre-commit run --all-files"
