#!/usr/bin/env bash
# exit on error
set -o errexit

# Обновляем pip
pip install --upgrade pip

# Устанавливаем зависимости
pip install -r requirements.txt

# Собираем статические файлы (важно для WhiteNoise)
echo "Starting collectstatic..."
python manage.py collectstatic --no-input --clear --verbosity 2

# Проверяем, что файлы собраны
echo "Checking static files..."
ls -la staticfiles/ | head -10
if [ -d "staticfiles/css" ]; then
    echo "CSS files found:"
    ls -la staticfiles/css/ | head -5
else
    echo "WARNING: staticfiles/css directory not found!"
fi
echo "Static files collection completed!"

# Применяем миграции
python manage.py migrate --no-input

# Создаем суперпользователя (опционально, можно сделать вручную через shell)
# python manage.py createsuperuser --noinput || true

