@echo off
chcp 65001 > nul
cls
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║         ДИАГНОСТИКА ЧАТА - ПОЛНАЯ ПРОВЕРКА             ║
echo ╚════════════════════════════════════════════════════════╝
echo.

echo [1/6] Проверка структуры проекта...
if exist "chat\models.py" (
    echo ✓ Приложение chat найдено
) else (
    echo ✗ ОШИБКА: Приложение chat не найдено!
    pause
    exit /b 1
)

echo.
echo [2/6] Проверка базы данных...
if exist "db.sqlite3" (
    echo ✓ База данных существует
) else (
    echo ✗ ВНИМАНИЕ: База данных не найдена
    echo   Запустите: full_reset_and_start.bat
)

echo.
echo [3/6] Проверка шаблона base.html...
findstr /C:"chat-widget-btn" templates\base.html > nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ Виджет чата найден в base.html
) else (
    echo ✗ ОШИБКА: Виджет чата не найден в base.html!
)

echo.
echo [4/6] Проверка WebSocket маршрутов...
findstr /C:"websocket_urlpatterns" chat\routing.py > nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ WebSocket маршруты настроены
) else (
    echo ✗ ОШИБКА: WebSocket маршруты не найдены!
)

echo.
echo [5/6] Проверка ASGI конфигурации...
findstr /C:"ProtocolTypeRouter" grocery_store\asgi.py > nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ ASGI настроен для WebSocket
) else (
    echo ✗ ОШИБКА: ASGI не настроен!
)

echo.
echo [6/6] Проверка кодировки файлов...
findstr /C:"# -*- coding: utf-8 -*-" chat\models.py > nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ Кодировка UTF-8 объявлена
) else (
    echo ⚠ ВНИМАНИЕ: Некоторые файлы могут не иметь объявления кодировки
)

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                  ИТОГОВАЯ ПРОВЕРКА                     ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo Проверяю настройки Django...
python manage.py check --tag chat 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✓ Django проверка пройдена успешно!
) else (
    echo.
    echo Полная проверка Django:
    python manage.py check
)

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                  СЛЕДУЮЩИЕ ШАГИ                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 1. Запустите сервер: start_server.bat
echo 2. Откройте браузер: http://127.0.0.1:8000/
echo 3. Войдите: admin / admin
echo 4. Найдите зеленую кнопку чата в правом нижнем углу
echo.
pause
