#!/bin/bash

set -e

SERVICE_NAME=$1

if [ "$SERVICE_NAME" = "django" ]; then
  python manage.py makemigrations
  python manage.py migrate
  python manage.py createsuperuser_if_none_exists \
    --username=$ADMIN_USERNAME \
    --password=$ADMIN_PASSWORD \
    --email=$ADMIN_EMAIL

  if [ "$DEBUG" = "True" ]; then
    python manage.py runserver 0.0.0.0:$PORT

  else
    python manage.py collectstatic --noinput
    gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers $GUNICORN_WORKERS \
    --worker-class gevent \
    --log-level DEBUG \
    --access-logfile "-" \
    --error-logfile "-" \
    $PROJECT_NAME.wsgi
  fi

# TODO: parameterize celery worker/beat options via env vars
elif [ "$SERVICE_NAME" = "celery" ]; then
  celery -A $PROJECT_NAME worker -P solo -c 1 -l info

elif [ "$SERVICE_NAME" = "beat" ]; then
  celery -A $PROJECT_NAME beat -l info

elif [ "$SERVICE_NAME" = "celery-beat" ]; then
  celery -A $PROJECT_NAME worker --beat -l info

elif [ "$SERVICE_NAME" = "flower" ]; then
  celery flower
  # celery \
  #   --app dockerapp.celery_app \
  #   flower \
  #   --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}" \
  #   --loglevel INFO
fi