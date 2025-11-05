#!/bin/sh
set -e

echo "Starting Eco-Mind Agent..."

APP_ENV=${APP_ENV:-development}

case "$APP_ENV" in
  development)
    echo "Running in development mode (hot reload enabled)"
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    ;;

  production)
    echo "Running in production mode (Gunicorn + Uvicorn workers)"
    exec gunicorn -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000 --workers 2
    ;;

  debug)
    echo "Starting in DEBUG mode — opening shell instead of server"
    exec /bin/sh
    ;;

  *)
    echo "Unknown APP_ENV: '$APP_ENV'. Please set to 'development', 'production', or 'debug'."
    exit 1
    ;;
esac
