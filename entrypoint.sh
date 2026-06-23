#!/bin/sh
set -e

# no override command given (the FastAPI app service) -> migrate then start granian
# otherwise (celery worker/beat/flower) -> just run whatever command: specified
if [ "$#" -eq 0 ]; then
    uv run alembic upgrade head
    exec uv run granian --interface asgi main:app --host 0.0.0.0 --port 8000
else
    exec "$@"
fi
