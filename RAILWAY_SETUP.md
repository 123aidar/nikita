# Настройка PostgreSQL на Railway

## Шаг 1: Создание PostgreSQL базы данных

1. Зайдите на [Railway](https://railway.app)
2. Откройте ваш проект `prodyktoviy1-production`
3. Нажмите **"+ New"** → **"Database"** → **"Add PostgreSQL"**
4. Railway автоматически создаст базу данных и сгенерирует переменные окружения

## Шаг 2: Проверка переменных окружения

После создания PostgreSQL, Railway автоматически добавит переменную `DATABASE_URL` к вашему сервису Django.

Проверьте в настройках проекта → Variables:
- `DATABASE_URL` должна иметь формат: `postgresql://user:password@host:port/database`

## Шаг 3: Деплой обновленного кода

```bash
# Закоммитьте изменения
git add .
git commit -m "Add PostgreSQL support"
git push
```

Railway автоматически пересоберет проект с новыми зависимостями.

## Шаг 4: Миграции базы данных

После успешного деплоя выполните миграции:

1. В Railway Dashboard откройте ваш сервис Django
2. Перейдите в **Settings** → **Deploy**
3. Найдите секцию **Run Command** и выполните:

```bash
python manage.py migrate
```

Или настройте автоматическое выполнение миграций при деплое:
- В настройках проекта добавьте **Start Command**:
```bash
python manage.py migrate && daphne -b 0.0.0.0 -p $PORT grocery_store.asgi:application
```

## Шаг 5: Создание суперпользователя

Чтобы создать администратора на production:

1. Откройте терминал в Railway (через Settings → Deploy → Open Shell)
2. Выполните:
```bash
python manage.py createsuperuser
```

Или используйте скрипт автоматического создания:
```bash
python create_superuser.py
```

## Шаг 6: Перенос данных (опционально)

Если у вас уже есть данные в SQLite и вы хотите их перенести:

### Экспорт данных из SQLite (локально):
```bash
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > data.json
```

### Импорт данных в PostgreSQL (на Railway):
```bash
python manage.py loaddata data.json
```

## Проверка работы

После завершения всех шагов:
1. Откройте ваш сайт: https://prodyktoviy1-production.up.railway.app
2. Войдите в админ панель: https://prodyktoviy1-production.up.railway.app/admin/
3. Проверьте, что данные сохраняются после перезапуска сервиса

## Переменные окружения (автоматически настроены Railway)

- `DATABASE_URL` - подключение к PostgreSQL
- `PORT` - порт для сервера (автоматически от Railway)

## Локальная разработка

Ваш проект теперь поддерживает оба режима:
- **Локально**: использует `db.sqlite3` (когда нет `DATABASE_URL`)
- **Railway**: использует PostgreSQL (когда есть `DATABASE_URL`)

Локально можно продолжать работать с SQLite без изменений.
