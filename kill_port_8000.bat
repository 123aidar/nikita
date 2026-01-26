@echo off
echo Завершение процессов на порту 8000...
echo.

:: Находим PID процесса на порту 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000.*LISTENING') do (
    echo Найден процесс PID: %%a
    taskkill /F /PID %%a 2>nul
    if errorlevel 1 (
        echo ОШИБКА: Требуются права администратора!
        echo Запустите этот файл от имени администратора ^(ПКМ -^> Запуск от имени администратора^)
    ) else (
        echo ✓ Процесс %%a завершен
    )
)

echo.
echo Готово!
timeout /t 2 >nul
