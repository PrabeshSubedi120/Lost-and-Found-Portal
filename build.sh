#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements_production.txt

cd lostfound_project
python manage.py collectstatic --noinput
python manage.py migrate

echo "Build completed successfully!"
