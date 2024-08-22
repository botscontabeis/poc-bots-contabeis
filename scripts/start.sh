#!/bin/bash

set -e

SERVICE_NAME=$1

CELERY_DEFAULT_LOG_LEVEL="INFO"

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

elif [ "$SERVICE_NAME" = "celery" ]; then
  COMMAND="celery -A $PROJECT_NAME worker"

  [ -n "$CELERY_BEAT" ] && COMMAND="$COMMAND -B"
  [ -n "$CELERY_POOL" ] && COMMAND="$COMMAND -P $CELERY_POOL"
  [ -n "$CELERY_CONCURRENCY" ] && COMMAND="$COMMAND -c $CELERY_CONCURRENCY"
  [ -n "$CELERY_LOG_LEVEL" ] && COMMAND="$COMMAND -l $CELERY_LOG_LEVEL" || COMMAND="$COMMAND -l $CELERY_DEFAULT_LOG_LEVEL"
  [ -n "$CELERY_MAX_TASKS_PER_CHILD" ] && COMMAND="$COMMAND --max-tasks-per-child=$CELERY_MAX_TASKS_PER_CHILD"

  echo "Running: $COMMAND"
  exec $COMMAND

elif [ "$SERVICE_NAME" = "beat" ]; then
  COMMAND="celery -A $PROJECT_NAME beat"
  [ -n "$CELERY_LOG_LEVEL" ] && COMMAND="$COMMAND -l $CELERY_LOG_LEVEL" || COMMAND="$COMMAND -l $CELERY_DEFAULT_LOG_LEVEL"

  echo "Running: $COMMAND"
  exec $COMMAND

elif [ "$SERVICE_NAME" = "flower" ]; then
  celery flower
fi
