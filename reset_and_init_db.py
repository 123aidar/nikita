# -*- coding: utf-8 -*-
"""
Скрипт для ПОЛНОЙ очистки и пересоздания БД на Railway
ВНИМАНИЕ: Удаляет ВСЕ данные!
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from accounts.models import CustomUser
from products.models import Category, Product
from sales.models import Sale
from inventory.models import Inventory

print("=" * 60)
print("ВНИМАНИЕ: ПОЛНАЯ ОЧИСТКА БАЗЫ ДАННЫХ")
print("=" * 60)

# Удаляем все данные
print("\n1. Удаление существующих данных...")
Sale.objects.all().delete()
print("   ✓ Продажи удалены")

Inventory.objects.all().delete()
print("   ✓ Инвентарь удален")

Product.objects.all().delete()
print("   ✓ Товары удалены")

Category.objects.all().delete()
print("   ✓ Категории удалены")

CustomUser.objects.all().delete()
print("   ✓ Пользователи удалены")

print("\n" + "=" * 60)
print("БАЗА ДАННЫХ ОЧИЩЕНА")
print("=" * 60)

# Запускаем полную инициализацию
print("\n" + "=" * 60)
print("НАЧИНАЕМ ЗАПОЛНЕНИЕ...")
print("=" * 60)

exec(open('init_production_db.py').read())

print("\n" + "=" * 60)
print("ДОБАВЛЕНИЕ РАСШИРЕННОГО КАТАЛОГА")
print("=" * 60)

exec(open('add_many_products.py').read())

print("\n" + "=" * 60)
print("ПЕРЕСОЗДАНИЕ ЗАВЕРШЕНО")
print(f"  • Пользователей: {CustomUser.objects.count()}")
print(f"  • Категорий: {Category.objects.count()}")
print(f"  • Товаров: {Product.objects.count()}")
print("\nДАННЫЕ ДЛЯ ВХОДА:")
print("  Менеджер: manager / manager")
print("  Кассир: cashier / cashier")
print("=" * 60)
