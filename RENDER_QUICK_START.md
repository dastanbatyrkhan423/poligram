# ⚡ Быстрый старт: Деплой на Render

## 🎯 ФИНАЛЬНАЯ START COMMAND:

```bash
gunicorn poligram_website.wsgi:application --bind 0.0.0.0:$PORT
```

## 📝 ОБЯЗАТЕЛЬНЫЕ ПЕРЕМЕННЫЕ ОКРУЖЕНИЯ:

Добавьте в Render Dashboard → Environment Variables:

```
SECRET_KEY=ваш-сгенерированный-ключ
DEBUG=False
ALLOWED_HOSTS=ваш-сайт.onrender.com,*.onrender.com
DATABASE_URL=postgresql://... (из настроек БД)
```

## 🔑 Как получить SECRET_KEY:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## ✅ Что изменено в коде:

1. ✅ `settings.py` - настроен для продакшена
2. ✅ `requirements.txt` - добавлен ckeditor uploader
3. ✅ `render.yaml` - обновлен start command
4. ✅ `build.sh` - улучшен скрипт сборки
5. ✅ Добавлены настройки безопасности для продакшена

## 🚀 Шаги деплоя:

1. Загрузите код на GitHub
2. Создайте PostgreSQL базу на Render
3. Создайте Web Service на Render
4. Установите переменные окружения (см. выше)
5. Build Command: `./build.sh`
6. Start Command: `gunicorn poligram_website.wsgi:application --bind 0.0.0.0:$PORT`
7. Задеплойте!

## 🐛 Если ошибка 500:

1. Установите `DEBUG=True` временно
2. Проверьте логи в Render Dashboard
3. Исправьте проблему
4. Верните `DEBUG=False`

Подробности: `RENDER_DEPLOY_FINAL.md`

