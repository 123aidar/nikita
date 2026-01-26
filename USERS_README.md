# Основные команды проекта

## Создание пользователей

```bash
python manage.py create_users
```

**Создаются:**
- Директор: `director / director123`
- Менеджер: `manager / manager123`
- Кассир: `cashier / cashier123`

## Работа с базой данных

### Создание миграций
```bash
python manage.py makemigrations
```

### Применение миграций
```bash
python manage.py migrate
```

### Сброс базы данных (полная перезагрузка)
```bash
# Удалить БД
del db.sqlite3

# Создать новую БД с миграциями
python manage.py migrate

# Создать пользователей
python manage.py create_users
```

## Запуск проекта

```bash
python manage.py runserver 8080
```

URL: http://127.0.0.1:8080/

## Вход в систему

URL входа: http://127.0.0.1:8080/accounts/login/

