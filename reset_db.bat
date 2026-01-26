@echo off
echo ========================================
echo Полное пересоздание базы данных
echo ========================================

REM Остановка Django сервера
echo.
echo [0/6] Проверяем запущенные процессы...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Administrator: python*" 2>nul
timeout /t 2 /nobreak >nul

REM Удаляем старую базу данных
echo.
echo [1/6] Удаляем базу данных...
if exist db.sqlite3 del /f /q db.sqlite3

REM Удаляем папку chat
echo [2/6] Удаляем папку chat...
if exist chat rmdir /s /q chat

REM Удаляем медиафайлы продуктов
echo [3/6] Удаляем медиафайлы продуктов...
if exist media\products rmdir /s /q media\products

REM Удаляем все миграции кроме __init__.py
echo [4/6] Удаляем старые миграции...
for /d %%d in (products\migrations sales\migrations accounts\migrations inventory\migrations reports\migrations) do (
    if exist %%d (
        for %%f in (%%d\*.py) do (
            if not "%%~nxf"=="__init__.py" (
                del /f /q "%%f"
            )
        )
    )
)

REM Создаем новые миграции
echo [5/6] Создаём новые миграции...
call venv\Scripts\activate.bat
python manage.py makemigrations

REM Применяем миграции
echo [6/6] Применяем миграции...
python manage.py migrate

echo.
echo ========================================
echo Готово! Теперь создайте суперпользователя:
echo python manage.py createsuperuser
echo ========================================
pause
