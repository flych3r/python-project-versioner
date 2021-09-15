#! /bin/bash

pipenv run alembic upgrade head
pipenv run uvicorn app.main:app --workers 1 --host 0.0.0.0 --port=${PORT:-5000}
