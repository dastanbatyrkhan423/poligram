# Инструкция по загрузке проекта на GitHub

## Способ 1: Через Personal Access Token (Рекомендуется)

1. **Создайте токен на GitHub:**
   - Перейдите: https://github.com/settings/tokens
   - Нажмите "Generate new token" → "Generate new token (classic)"
   - Название: `Poligram Deploy`
   - Выберите scope: `repo` (полный доступ)
   - Нажмите "Generate token"
   - **Скопируйте токен** (показывается только один раз!)

2. **Выполните команду в терминале:**
   ```bash
   git push -u origin main
   ```
   
   Когда попросит логин/пароль:
   - **Username**: ваш GitHub username (citatydusi-sys)
   - **Password**: вставьте токен (НЕ ваш пароль!)

## Способ 2: Через GitHub Desktop

1. Скачайте GitHub Desktop: https://desktop.github.com/
2. Войдите в аккаунт citatydusi-sys
3. File → Add Local Repository
4. Выберите папку проекта
5. Нажмите "Publish repository"

## Способ 3: Через SSH ключ

1. **Создайте SSH ключ (если нет):**
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **Скопируйте публичный ключ:**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

3. **Добавьте ключ на GitHub:**
   - Перейдите: https://github.com/settings/keys
   - Нажмите "New SSH key"
   - Вставьте скопированный ключ
   - Сохраните

4. **Измените remote на SSH:**
   ```bash
   git remote set-url origin git@github.com:citatydusi-sys/Poligram.git
   git push -u origin main
   ```

## Текущий статус

✅ Git репозиторий инициализирован
✅ Все файлы добавлены в commit
✅ Remote origin настроен
⏳ Ожидается авторизация для push

## После успешного push

Ваш проект будет доступен по адресу:
https://github.com/citatydusi-sys/Poligram

