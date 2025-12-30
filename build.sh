#!/usr/bin/env bash
# exit on error
set -o errexit

# Обновляем pip
pip install --upgrade pip

# Устанавливаем зависимости
pip install -r requirements.txt

# Собираем статические файлы (важно для WhiteNoise)
python manage.py collectstatic --no-input --clear

# Проверяем, что файлы собраны
echo "Checking static files..."
ls -la staticfiles/ || echo "Static files directory created"

# Применяем миграции
python manage.py migrate --no-input

# Создаем суперпользователя (опционально, можно сделать вручную через shell)
# python manage.py createsuperuser --noinput || true

