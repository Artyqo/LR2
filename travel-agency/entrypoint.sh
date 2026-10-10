#!/usr/bin/env bash
set -o errexit

echo "Устанавливаем зависимости..."
pip install -r requirements.txt

echo "Собираем статику..."
python manage.py collectstatic --no-input

echo "Применяем миграции..."
python manage.py migrate

echo "Создаём суперпользователя если не существует..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('Суперпользователь создан: admin / admin123')
else:
    print('Суперпользователь уже существует')
"

echo "Запускаем gunicorn..."
exec gunicorn travel_agency.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 2 \
    --timeout 120