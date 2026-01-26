#!/bin/bash

echo "========================================"
echo "  Продуктовый магазин - Запуск сервера"
echo "========================================"
echo ""

echo "Проверка виртуального окружения..."
if [ ! -d "venv" ]; then
    echo "Виртуальное окружение не найдено. Создаю..."
    python3 -m venv venv
    echo "Виртуальное окружение создано."
    echo ""
fi

echo "Активация виртуального окружения..."
source venv/bin/activate

echo "Установка зависимостей..."
pip install -r requirements.txt --quiet

echo ""
echo "Применение миграций..."
python manage.py migrate

echo ""
echo "========================================"
echo "  Сервер запускается..."
echo "  Откройте браузер: http://localhost:8000"
echo "========================================"
echo ""

python manage.py runserver
