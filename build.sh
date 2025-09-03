#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements_production.txt

cd lostfound_project
python manage.py collectstatic --noinput
python manage.py migrate

# Create superuser if it doesn't exist (non-interactive)
echo "from django.contrib.auth.models import User; User.objects.filter(is_superuser=True).exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123456')" | python manage.py shell
