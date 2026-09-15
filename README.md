# fastapi-tasks

A FastAPI task API in a Docker container; every task is stored in a Back4app backend over REST. Companion to the Back4app blog post on deploying a Python app from a Dockerfile with a database and no servers to manage.

Run locally: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`, `cp .env.example .env`, then `set -a; . ./.env; set +a; .venv/bin/uvicorn main:app --port 8000`.
