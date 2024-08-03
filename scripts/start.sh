#!/bin/bash

set -e

PROCESS_TYPE=$1

if [ "$PROCESS_TYPE" = "django" ]; then
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

elif [ "$PROCESS_TYPE" = "celery" ]; then
  celery -A $PROJECT_NAME worker -l info

elif [ "$PROCESS_TYPE" = "beat" ]; then
  celery -A $PROJECT_NAME beat -l info

elif [ "$PROCESS_TYPE" = "celery-beat" ]; then
  celery -A $PROJECT_NAME worker --beat -l info

elif [ "$PROCESS_TYPE" = "flower" ]; then
  celery flower
  # celery \
  #   --app dockerapp.celery_app \
  #   flower \
  #   --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}" \
  #   --loglevel INFO
