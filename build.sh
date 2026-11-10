#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py makemigrations accounts inventory shelves sales payments suppliers expenses reports audit
python manage.py migrate
python manage.py seed_data
