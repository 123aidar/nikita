@echo off
chcp 65001
echo.
echo ============================================
echo ПРОВЕРКА НАСТРОЕК ЧАТА
echo ============================================
echo.
echo 1. Проверка установки Django Channels...
python -c "import channels; print('✓ Django Channels установлен, версия:', channels.__version__)"
echo.
echo 2. Проверка установки Daphne...
python -c "import daphne; print('✓ Daphne установлен, версия:', daphne.__version__)"
echo.
echo 3. Проверка модели сообщений...
python manage.py shell -c "from chat.models import Message; print('✓ Модель Message доступна'); print('  Всего сообщений:', Message.objects.count())"
echo.
echo 4. Проверка WebSocket маршрутов...
python manage.py shell -c "from chat.routing import websocket_urlpatterns; print('✓ WebSocket маршруты настроены'); print('  Маршрутов:', len(websocket_urlpatterns))"
echo.
echo 5. Проверка ASGI конфигурации...
python manage.py shell -c "from grocery_store.asgi import application; print('✓ ASGI приложение настроено')"
echo.
echo ============================================
echo Все проверки завершены!
echo ============================================
echo.
echo ВАЖНО: Для работы чата запустите сервер с помощью:
echo   python manage.py runserver
echo.
echo (НЕ используйте manage.py runserver с --noreload)
echo.
pause
