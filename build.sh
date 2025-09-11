#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements_production.txt

cd lostfound_project
python manage.py collectstatic --noinput
python manage.py migrate

# Clean up unwanted admin users
echo "Cleaning up unwanted admin users..."
python manage.py remove_unwanted_admin --username admin --confirm || echo "No unwanted admin users found"

echo "Build completed successfully!"
