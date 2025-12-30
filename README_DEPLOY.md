# Инструкция по деплою на Render

## Подготовка к деплою

1. **Создайте аккаунт на Render.com**
   - Зайдите на https://render.com
   - Зарегистрируйтесь или войдите

2. **Подготовьте репозиторий**
   - Загрузите код в GitHub/GitLab/Bitbucket
   - Убедитесь, что все файлы закоммичены

## Деплой через Render Dashboard

### Шаг 1: Создание базы данных

1. В Dashboard Render нажмите "New +" → "PostgreSQL"
2. Настройки:
   - **Name**: `poligram-db`
   - **Database**: `poligram`
   - **User**: `poligram_user`
   - **Region**: выберите ближайший (например, Frankfurt)
   - **Plan**: Starter (бесплатный)
3. Нажмите "Create Database"
4. После создания скопируйте **Internal Database URL**

### Шаг 2: Создание Web Service

1. В Dashboard нажмите "New +" → "Web Service"
2. Подключите ваш репозиторий
3. Настройки:
   - **Name**: `poligram-website`
   - **Region**: тот же, что и база данных
   - **Branch**: `main` (или ваша основная ветка)
   - **Root Directory**: оставьте пустым
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn poligram_website.wsgi:application`

### Шаг 3: Настройка переменных окружения

В разделе "Environment" добавьте:

```
SECRET_KEY=ваш-секретный-ключ-здесь
DEBUG=False
ALLOWED_HOSTS=ваш-сайт.onrender.com
DATABASE_URL=внутренний-url-базы-данных-из-шага-1
```

**Как получить SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Шаг 4: Деплой

1. Нажмите "Create Web Service"
2. Render автоматически начнет деплой
3. Дождитесь завершения (обычно 5-10 минут)

## Альтернативный способ: через render.yaml

Если вы используете `render.yaml`:

1. Убедитесь, что файл `render.yaml` в корне проекта
2. В Dashboard Render нажмите "New +" → "Blueprint"
3. Подключите репозиторий
4. Render автоматически создаст все сервисы из `render.yaml`

## После деплоя

1. **Создайте суперпользователя:**
   - В Render Dashboard откройте ваш Web Service
   - Перейдите в "Shell"
   - Выполните:
   ```bash
   python manage.py createsuperuser
   ```

2. **Проверьте сайт:**
   - Откройте URL вашего сайта (например: `https://poligram-website.onrender.com`)
   - Убедитесь, что все работает

3. **Настройте домен (опционально):**
   - В настройках Web Service → "Custom Domains"
   - Добавьте ваш домен

## Важные замечания

- **Бесплатный план Render** может "засыпать" после 15 минут бездействия
- Первый запрос после "сна" может занять 30-60 секунд
- Для продакшена рекомендуется использовать платный план

## Локальная разработка

Для локальной разработки создайте файл `.env`:

```bash
cp .env.example .env
```

И заполните его своими значениями.

