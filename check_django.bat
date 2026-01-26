@echo off
chcp 65001 > nul
cd /d d:\1
echo Проверка Django...
python manage.py check
echo.
echo Проверка завершена!
pause
