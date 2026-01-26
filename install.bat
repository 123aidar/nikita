@echo off
echo ============================================
echo   Полная установка проекта
echo ============================================
echo.

echo [1/6] Создание виртуального окружения...
if not exist "venv\" (
    python -m venv venv
    echo ✓ Виртуальное окружение создано
) else (
    echo ✓ Виртуальное окружение уже существует
)
echo.

echo [2/6] Активация виртуального окружения...
call venv\Scripts\activate.bat
echo.

echo [3/6] Установка зависимостей...
pip install -r requirements.txt
echo ✓ Зависимости установлены
echo.

echo [4/6] Создание миграций...
python manage.py makemigrations
echo ✓ Миграции созданы
echo.

echo [5/6] Применение миграций...
python manage.py migrate
echo ✓ База данных настроена
echo.

echo [6/6] Создание начальных данных...
python manage.py setup_initial_data
echo.

echo [7/7] Создание суперпользователя...
echo Введите данные для администратора:
python manage.py createsuperuser
echo.

echo ============================================
echo   Установка завершена!
echo ============================================
echo.
echo Для запуска сервера используйте: start.bat
echo или команду: python manage.py runserver
echo.
echo Хотите создать тестовые данные? (y/n)
set /p answer=

if /i "%answer%"=="y" (
    echo.
    echo Создание тестовых данных...
    python manage.py shell < create_test_data.py
    echo.
    echo ✓ Тестовые данные созданы!
    echo.
    echo Тестовые аккаунты:
    echo   director / director123
    echo   manager / manager123
    echo   cashier / cashier123
)

echo.
pause
