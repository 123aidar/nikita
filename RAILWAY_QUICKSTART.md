# Быстрая настройка PostgreSQL на Railway

## ⚡ Что сделано

✅ Добавлена поддержка PostgreSQL в коде
✅ Обновлены зависимости (psycopg2-binary, dj-database-url)
✅ **Исправлена версия Pillow (11.1.0) для совместимости с Python 3.13**
✅ **Настроен Daphne ASGI сервер для WebSocket поддержки**
✅ Создана конфигурация для Railway (Procfile, railway.toml, nixpacks.toml)
✅ Настроено автоматическое переключение: SQLite локально, PostgreSQL на Railway
✅ **Код отправлен в репозиторий:** https://github.com/error04p124124/ProdyktoviyFinaly

## 🚀 Что нужно сделать на Railway

### 1️⃣ Добавить PostgreSQL базу данных

В вашем проекте на Railway:
```
1. Нажмите "+ New" → "Database" → "Add PostgreSQL"
2. Railway автоматически создаст переменную DATABASE_URL
3. Подождите пока БД создастся (1-2 минуты)
```

### 2️⃣ Задеплоить обновленный код

```bash
git add .
git commit -m "Add PostgreSQL support"
git push origin main
```

Railway автоматически (через GitHub webhook):
- Установит новые зависимости
- Выполнит миграции базы данных
- Запустит сервер с Daphne

**Репозиторий:** https://github.com/error04p124124/ProdyktoviyFinaly

### 3️⃣ Создать суперпользователя (опционально)

Вариант А - через Railway Shell:
```
1. Откройте ваш сервис в Railway
2. Settings → Deploy → "Open Shell"
3. Выполните: python manage.py createsuperuser
```

Вариант Б - автоматически через скрипт:
```bash
# На Railway выполните:
python create_superuser.py
```

## ✅ Готово!

Теперь все данные сохраняются в PostgreSQL и не теряются при перезапуске.

Откройте: https://prodyktoviy1-production.up.railway.app

---

## 📝 Полная инструкция

См. [RAILWAY_SETUP.md](RAILWAY_SETUP.md) для детальной информации о переносе данных и решении проблем.
