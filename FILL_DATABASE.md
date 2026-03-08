# 🚀 База данных пуста - как заполнить

## Проблема
После деплоя на Railway база данных PostgreSQL пустая - нет пользователей, категорий, товаров.

## ✅ Решение за 3 шага

### Шаг 1: Проверьте PostgreSQL на Railway

1. Откройте Railway Dashboard: https://railway.app
2. Откройте ваш проект **striking-grace**
3. **Важно!** Должны быть **2 сервиса**:
   - 🟢 Django приложение (ваш код)
   - 🟢 PostgreSQL база данных

**Если PostgreSQL НЕТ:**
```
Нажмите "+ New" → "Database" → "Add PostgreSQL"
```
Railway автоматически создаст переменную `DATABASE_URL` и свяжет её с Django.

### Шаг 2: Проверьте миграции

1. Откройте ваш Django сервис
2. Перейдите в **Deployments**
3. Посмотрите **Deploy Logs**
4. Должна быть строка:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying accounts.0001_initial... OK
  ...
```

**Если миграций нет**, выполните вручную через Shell (см. Шаг 3).

### Шаг 3: Заполните базу данных

1. Откройте ваш Django сервис в Railway
2. Перейдите: **Settings** → нажмите три точки **"..."** → **Shell**
3. В открывшемся терминале выполните:

```bash
# Если миграции не выполнены
python manage.py migrate

# Заполнить базу данных
python init_production_db.py
```

**Что создаст скрипт:**
- ✅ Администратор (admin / admin)
- ✅ Кассир (cashier / cashier)
- ✅ 6 категорий товаров
- ✅ 20 товаров со штрих-кодами

### Шаг 4: Проверьте сайт

Откройтеваш сайт и войдите:
- **Логин:** admin
- **Пароль:** admin

Вы увидите все товары и категории!

---

## 🔧 Альтернативный способ (если Shell не работает)

Можно выполнить команды через Railway CLI:

```bash
# Установите Railway CLI
npm i -g @railway/cli

# Войдите
railway login

# Подключитесь к проекту
railway link

# Выполните миграции
railway run python manage.py migrate

# Заполните базу
railway run python init_production_db.py
```

---

## ❓ Часто возникающие проблемы

### "No module named 'products'"
**Решение:** Убедитесь, что деплой завершился успешно. Проверьте Build Logs.

### "relation does not exist"
**Решение:** Миграции не выполнены. Запустите `python manage.py migrate`

### "DATABASE_URL not set"
**Решение:** PostgreSQL не добавлен. Добавьте через Railway Dashboard.

---

## 📝 Для локальной разработки

Локально база данных будет отдельная (SQLite). Чтобы заполнить локально:

```bash
python init_production_db.py
```

Или используйте более полный скрипт:

```bash
python setup_data.py
```
