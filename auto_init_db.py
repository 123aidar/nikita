# -*- coding: utf-8 -*-
"""
Полная инициализация БД при первом запуске
Удаляет старые данные и создает новые
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from accounts.models import CustomUser
from products.models import Category, Product

print("=" * 60)
print("ПОЛНАЯ ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ")
print("=" * 60)

# Проверяем нужна ли инициализация
if CustomUser.objects.count() == 0 and Product.objects.count() == 0:
    print("\nБД пустая - начинаем заполнение...")
    
    # Запускаем базовую инициализацию (пользователи + базовые категории и товары)
    exec(open('init_production_db.py').read())
    
    # Добавляем расширенный каталог товаров
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
    print("\n✓ База данных уже заполнена")
    print(f"  • Пользователей: {CustomUser.objects.count()}")
    print(f"  • Категорий: {Category.objects.count()}")
    print(f"  • Товаров: {Product.objects.count()}")
