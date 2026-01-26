@echo off
echo ========================================
echo Создание тестовых данных
echo ========================================

call venv\Scripts\activate.bat

echo.
echo Создаём данные через Django management command...
python manage.py create_test_data

echo.
echo ========================================
echo Готово! Данные созданы.
echo Логин: admin
echo Пароль: admin123
echo ========================================
pause
