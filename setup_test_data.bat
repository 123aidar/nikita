@echo off
echo ========================================
echo   Создание тестовых данных
echo ========================================
echo.

call venv\Scripts\activate.bat

echo Создание тестовых данных...
python manage.py shell < create_test_data.py

echo.
echo Готово! Тестовые данные созданы.
pause
