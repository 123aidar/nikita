@echo off
echo ========================================
echo   Продуктовый магазин - Запуск сервера
echo ========================================
echo.

echo Проверка виртуального окружения...
if not exist "venv\" (
    echo Виртуальное окружение не найдено. Создаю...
    python -m venv venv
    echo Виртуальное окружение создано.
    echo.
)

echo Активация виртуального окружения...
call venv\Scripts\activate.bat

echo Установка зависимостей...
pip install -r requirements.txt --quiet

echo.
echo Применение миграций...
python manage.py migrate

echo.
echo ========================================
echo   Сервер запускается...
echo   Откройте браузер: http://localhost:8000
echo ========================================
echo.

python manage.py runserver
