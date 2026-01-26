@echo off
chcp 65001
echo.
echo ============================================
echo ПОЛНЫЙ СБРОС И ЗАПУСК С ПРОВЕРКОЙ ЧАТА
echo ============================================
echo.

echo Шаг 1: Удаление базы данных...
if exist db.sqlite3 del /Q db.sqlite3

echo Шаг 2: Удаление миграций...
for /d %%d in (accounts\migrations products\migrations sales\migrations inventory\migrations reports\migrations chat\migrations) do (
    if exist "%%d" (
        for %%f in ("%%d\*.py") do (
            if not "%%~nf"=="__init__" del /Q "%%f"
        )
    )
)

echo Шаг 3: Создание новых миграций...
python manage.py makemigrations

echo Шаг 4: Применение миграций...
python manage.py migrate

echo Шаг 5: Создание суперпользователя...
python create_superuser.py

echo Шаг 6: Создание тестовых данных...
python manage.py create_test_data

echo.
echo ============================================
echo База данных готова!
echo ============================================
echo.
echo Логин: admin
echo Пароль: admin
echo.
echo Запускаю сервер для проверки чата...
echo После запуска откройте: http://127.0.0.1:8080/
echo.
python manage.py runserver 8080
