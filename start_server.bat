@echo off
chcp 65001
cls
echo ╔════════════════════════════════════════════════════════╗
echo ║      Запуск сервера Django с WebSocket поддержкой     ║
echo ╚════════════════════════════════════════════════════════╝
echo.

:: Проверка, не занят ли порт 8000
netstat -ano | findstr :8000.*LISTENING >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ⚠ ВНИМАНИЕ: Порт 8000 уже занят!
    echo.
    echo Выберите действие:
    echo [1] Попробовать завершить процесс на порту 8000
    echo [2] Запустить на альтернативном порту 8080
    echo [3] Выход
    echo.
    choice /C 123 /N /M "Ваш выбор (1-3): "
    
    if errorlevel 3 exit /b
    if errorlevel 2 (
        echo.
        echo Запускаю на порту 8080...
        echo После запуска откройте: http://127.0.0.1:8080/
        echo.
        python manage.py runserver 8080
        exit /b
    )
    if errorlevel 1 (
        echo.
        echo Завершаю процесс на порту 8000...
        for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000.*LISTENING') do (
            taskkill /F /PID %%a >nul 2>&1
            if errorlevel 1 (
                echo ✗ Требуются права администратора!
                echo   Запустите kill_port_8000.bat от имени администратора
                echo   или используйте порт 8080
                pause
                exit /b 1
            )
        )
        echo ✓ Порт освобожден
        echo.
        timeout /t 2 >nul
    )
)

echo Запускаю Django сервер с WebSocket поддержкой на порту 8000...
echo После запуска откройте: http://127.0.0.1:8000/
echo.
echo Используется Daphne ASGI сервер для поддержки WebSocket
echo.
venv\Scripts\daphne.exe -b 127.0.0.1 -p 8000 grocery_store.asgi:application
