# -*- coding: utf-8 -*-
"""
Автоматическая инициализация БД если она пустая
Вызывается после миграций при деплое
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from accounts.models import CustomUser
from products.models import Category, Product

# Проверяем есть ли данные
if CustomUser.objects.count() == 0 and Category.objects.count() == 0:
    print("=" * 60)
    print("БД ПУСТАЯ - АВТОМАТИЧЕСКОЕ ЗАПОЛНЕНИЕ")
    print("=" * 60)
    
    # Запускаем скрипт инициализации
    exec(open('init_production_db.py').read())
    
    # Добавляем расширенный ассортимент (быстрая массовая вставка)
    print("\n" + "=" * 60)
    print("ЗАГРУЗКА РАСШИРЕННОГО КАТАЛОГА")
    print("=" * 60)
    exec(open('add_many_products.py').read())
    
    print("\n" + "=" * 60)
    print("ИНИЦИАЛИЗАЦИЯ ЗАВЕРШЕНА")
    print(f"  • Пользователей: {CustomUser.objects.count()}")
    print(f"  • Категорий: {Category.objects.count()}")
    print(f"  • Товаров: {Product.objects.count()}")
    print("=" * 60)
else:
    print("✓ База данных уже заполнена")
    print(f"  • Пользователей: {CustomUser.objects.count()}")
    print(f"  • Категорий: {Category.objects.count()}")
    print(f"  • Товаров: {Product.objects.count()}")
