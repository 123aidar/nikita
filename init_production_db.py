# -*- coding: utf-8 -*-
"""
Скрипт для быстрого заполнения базы данных на Railway
Создает администратора, категории и несколько тестовых товаров
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from accounts.models import CustomUser
from products.models import Category, Product
from decimal import Decimal

print("=" * 60)
print("ЗАПОЛНЕНИЕ БАЗЫ ДАННЫХ")
print("=" * 60)

# 1. Создание администратора
print("\n1. Создание администратора...")
CustomUser.objects.filter(username='admin').delete()
admin = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@store.com',
    password='admin',
    first_name='Администратор',
    last_name='Системы',
    phone='+79991234567',
    role='manager'
)
print(f"   ✓ Администратор создан: {admin.get_full_name()}")
print(f"   Логин: admin")
print(f"   Пароль: admin")

# 2. Создание кассира
print("\n2. Создание кассира...")
CustomUser.objects.filter(username='cashier').delete()
cashier = CustomUser.objects.create_user(
    username='cashier',
    email='cashier@store.com',
    password='cashier',
    first_name='Иван',
    last_name='Кассиров',
    phone='+79991234568',
    role='cashier'
)
print(f"   ✓ Кассир создан: {cashier.get_full_name()}")
print(f"   Логин: cashier")
print(f"   Пароль: cashier")

# 3. Создание категорий
print("\n3. Создание категорий...")
categories_data = [
    ('Овощи и фрукты', 'fa-carrot', 'Свежие овощи и фрукты'),
    ('Молочные продукты', 'fa-cheese', 'Молоко, сыр, йогурты'),
    ('Мясо и птица', 'fa-drumstick-bite', 'Свежее мясо'),
    ('Хлебобулочные изделия', 'fa-bread-slice', 'Хлеб и выпечка'),
    ('Напитки', 'fa-bottle-water', 'Вода, соки, газировка'),
    ('Крупы', 'fa-seedling', 'Крупы и макароны'),
]

categories = {}
for name, icon, desc in categories_data:
    cat, created = Category.objects.get_or_create(
        name=name,
        defaults={'icon': icon, 'description': desc}
    )
    categories[name] = cat
    print(f"   ✓ {name}")

# 4. Создание товаров
print("\n4. Создание товаров...")
products_data = [
    # Овощи и фрукты
    ('Овощи и фрукты', 'Яблоки Гала', 150.00, 'кг', 50, '4011200296908'),
    ('Овощи и фрукты', 'Бананы', 120.00, 'кг', 30, '4011200314401'),
    ('Овощи и фрукты', 'Помидоры', 250.00, 'кг', 25, '4011200314418'),
    ('Овощи и фрукты', 'Огурцы', 180.00, 'кг', 40, '4011200314425'),
    
    # Молочные продукты
    ('Молочные продукты', 'Молоко 2.5%', 85.00, 'л', 60, '4605246003011'),
    ('Молочные продукты', 'Кефир 1%', 75.00, 'л', 45, '4605246003028'),
    ('Молочные продукты', 'Сметана 20%', 120.00, 'кг', 30, '4605246003035'),
    ('Молочные продукты', 'Сыр Российский', 450.00, 'кг', 20, '4605246003042'),
    
    # Мясо и птица
    ('Мясо и птица', 'Куриная грудка', 380.00, 'кг', 25, '4607034370015'),
    ('Мясо и птица', 'Свинина', 450.00, 'кг', 20, '4607034370022'),
    ('Мясо и птица', 'Говядина', 550.00, 'кг', 15, '4607034370039'),
    
    # Хлебобулочные изделия
    ('Хлебобулочные изделия', 'Хлеб белый', 45.00, 'шт', 100, '4606272003015'),
    ('Хлебобулочные изделия', 'Хлеб черный', 50.00, 'шт', 80, '4606272003022'),
    ('Хлебобулочные изделия', 'Батон', 40.00, 'шт', 70, '4606272003039'),
    
    # Напитки
    ('Напитки', 'Вода минеральная', 55.00, 'л', 120, '4602480003011'),
    ('Напитки', 'Сок апельсиновый', 95.00, 'л', 60, '4602480003028'),
    ('Напитки', 'Газировка Кола', 85.00, 'л', 80, '4602480003035'),
    
    # Крупы
    ('Крупы', 'Гречка', 95.00, 'кг', 100, '4607017223017'),
    ('Крупы', 'Рис круглозерный', 85.00, 'кг', 120, '4607017223024'),
    ('Крупы', 'Макароны спагетти', 70.00, 'кг', 90, '4607017223031'),
]

for cat_name, prod_name, price, unit, stock, barcode in products_data:
    product, created = Product.objects.get_or_create(
        name=prod_name,
        defaults={
            'category': categories[cat_name],
            'price': Decimal(str(price)),
            'unit': unit,
            'quantity': stock,
            'barcode': barcode,
            'description': f'{prod_name} - высокое качество'
        }
    )
    if created:
        print(f"   ✓ {prod_name} ({barcode})")

print("\n" + "=" * 60)
print("БАЗА ДАННЫХ УСПЕШНО ЗАПОЛНЕНА")
print("=" * 60)
print("\nСОЗДАНО:")
print(f"  • Пользователей: {CustomUser.objects.count()}")
print(f"  • Категорий: {Category.objects.count()}")
print(f"  • Товаров: {Product.objects.count()}")
print("\nДЛЯ ВХОДА В СИСТЕМУ:")
print("  Администратор - admin / admin")
print("  Кассир - cashier / cashier")
print("=" * 60)
