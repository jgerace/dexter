#!/bin/bash
set -e

# Generate SECRET_KEY if it doesn't exist
if [ -z "$DJANGO_SECRET_KEY" ]; then
    export DJANGO_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')
fi

# Run migrations and collect static files (if applicable)
python manage.py makemigrations
python manage.py migrate --noinput
python manage.py collectstatic --noinput

# Start the Django server
exec "$@"