@echo off
chcp 65001 >nul
echo ========================================
echo ПОЛНЫЙ СБРОС БАЗЫ ДАННЫХ
echo ========================================
echo.
echo ВАЖНО: Закройте сервер (Ctrl+C) перед запуском!
echo.
pause

cd /d D:\1
call venv\Scripts\activate.bat

echo.
echo [1/5] Останавливаем все процессы Python...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo [2/5] Удаляем старую базу данных...
del /f /q db.sqlite3 2>nul

echo [3/5] Удаляем папку chat...
if exist chat rmdir /s /q chat

echo [4/5] Удаляем все миграции...
for /d %%d in (products\migrations sales\migrations accounts\migrations inventory\migrations reports\migrations) do (
    if exist %%d (
        for %%f in (%%d\*.py) do (
            if not "%%~nxf"=="__init__.py" (
                del /f /q "%%f"
            )
        )
    )
)

echo [5/5] Создаём новые миграции и базу...
python manage.py makemigrations
python manage.py migrate

echo.
echo ========================================
echo ГОТОВО! Теперь запустите create_data.bat
echo ========================================
pause
