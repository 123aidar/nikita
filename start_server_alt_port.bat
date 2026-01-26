@echo off
chcp 65001
echo Запуск сервера Django на альтернативном порту 8080...
echo.
echo После запуска откройте в браузере: http://127.0.0.1:8080/
echo.
python manage.py runserver 8080
