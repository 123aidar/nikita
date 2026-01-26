# -*- coding: utf-8 -*-
"""
Скрипт для создания тестовых данных для продуктового магазина
Запуск: python manage.py shell < create_test_data.py
"""

from accounts.models import CustomUser
from products.models import Category, Product
from django.utils import timezone
from datetime import timedelta
import random

print("Создание тестовых данных...")

# Создание категорий
categories_data = [
    {'name': 'Овощи', 'icon': 'fa-carrot', 'description': 'Свежие овощи'},
    {'name': 'Фрукты', 'icon': 'fa-apple-alt', 'description': 'Свежие фрукты'},
    {'name': 'Молочные продукты', 'icon': 'fa-cheese', 'description': 'Молоко, сыр, йогурты'},
    {'name': 'Мясо и птица', 'icon': 'fa-drumstick-bite', 'description': 'Свежее мясо'},
    {'name': 'Хлебобулочные изделия', 'icon': 'fa-bread-slice', 'description': 'Хлеб, булки'},
    {'name': 'Напитки', 'icon': 'fa-wine-bottle', 'description': 'Соки, вода, газировка'},
    {'name': 'Крупы', 'icon': 'fa-box', 'description': 'Гречка, рис, макароны'},
    {'name': 'Консервы', 'icon': 'fa-fish', 'description': 'Консервированные продукты'},
]

categories = []
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={'icon': cat_data['icon'], 'description': cat_data['description']}
    )
    categories.append(category)
    if created:
        print(f"✓ Создана категория: {category.name}")

# Создание пользователей
users_data = [
    {
        'username': 'director',
        'password': 'director123',
        'first_name': 'Иван',
        'last_name': 'Петров',
        'role': 'director',
        'email': 'director@shop.ru',
        'phone': '+7 (999) 123-45-67'
    },
    {
        'username': 'manager',
        'password': 'manager123',
        'first_name': 'Мария',
        'last_name': 'Сидорова',
        'role': 'manager',
        'email': 'manager@shop.ru',
        'phone': '+7 (999) 234-56-78'
    },
    {
        'username': 'cashier',
        'password': 'cashier123',
        'first_name': 'Анна',
        'last_name': 'Иванова',
        'role': 'cashier',
        'email': 'cashier@shop.ru',
        'phone': '+7 (999) 345-67-89'
    },
]

users = []
for user_data in users_data:
    password = user_data.pop('password')
    user, created = CustomUser.objects.get_or_create(
        username=user_data['username'],
        defaults=user_data
    )
    if created:
        user.set_password(password)
        user.save()
        print(f"✓ Создан пользователь: {user.username} ({user.get_role_display()}) - пароль: {password}")
    users.append(user)

# Создание товаров
products_data = [
    # Овощи
    {'name': 'Картофель', 'category': 'Овощи', 'price': 35.50, 'quantity': 150, 'unit': 'кг'},
    {'name': 'Морковь', 'category': 'Овощи', 'price': 42.00, 'quantity': 80, 'unit': 'кг'},
    {'name': 'Лук репчатый', 'category': 'Овощи', 'price': 28.00, 'quantity': 100, 'unit': 'кг'},
    {'name': 'Помидоры', 'category': 'Овощи', 'price': 185.00, 'quantity': 50, 'unit': 'кг'},
    {'name': 'Огурцы', 'category': 'Овощи', 'price': 165.00, 'quantity': 45, 'unit': 'кг'},
    {'name': 'Капуста', 'category': 'Овощи', 'price': 32.00, 'quantity': 120, 'unit': 'кг'},
    
    # Фрукты
    {'name': 'Яблоки', 'category': 'Фрукты', 'price': 95.00, 'quantity': 80, 'unit': 'кг'},
    {'name': 'Бананы', 'category': 'Фрукты', 'price': 78.00, 'quantity': 60, 'unit': 'кг'},
    {'name': 'Апельсины', 'category': 'Фрукты', 'price': 125.00, 'quantity': 55, 'unit': 'кг'},
    {'name': 'Груши', 'category': 'Фрукты', 'price': 115.00, 'quantity': 45, 'unit': 'кг'},
    
    # Молочные продукты
    {'name': 'Молоко 3.2%', 'category': 'Молочные продукты', 'price': 85.00, 'quantity': 100, 'unit': 'л'},
    {'name': 'Кефир', 'category': 'Молочные продукты', 'price': 75.00, 'quantity': 80, 'unit': 'л'},
    {'name': 'Сметана 20%', 'category': 'Молочные продукты', 'price': 145.00, 'quantity': 50, 'unit': 'кг'},
    {'name': 'Сыр Российский', 'category': 'Молочные продукты', 'price': 485.00, 'quantity': 30, 'unit': 'кг'},
    
    # Мясо
    {'name': 'Говядина', 'category': 'Мясо и птица', 'price': 485.00, 'quantity': 40, 'unit': 'кг'},
    {'name': 'Свинина', 'category': 'Мясо и птица', 'price': 395.00, 'quantity': 50, 'unit': 'кг'},
    {'name': 'Курица', 'category': 'Мясо и птица', 'price': 245.00, 'quantity': 70, 'unit': 'кг'},
    
    # Хлеб
    {'name': 'Хлеб белый', 'category': 'Хлебобулочные изделия', 'price': 45.00, 'quantity': 100, 'unit': 'шт'},
    {'name': 'Хлеб черный', 'category': 'Хлебобулочные изделия', 'price': 42.00, 'quantity': 100, 'unit': 'шт'},
    {'name': 'Батон', 'category': 'Хлебобулочные изделия', 'price': 38.00, 'quantity': 80, 'unit': 'шт'},
    
    # Напитки
    {'name': 'Вода минеральная', 'category': 'Напитки', 'price': 45.00, 'quantity': 200, 'unit': 'л'},
    {'name': 'Сок апельсиновый', 'category': 'Напитки', 'price': 125.00, 'quantity': 100, 'unit': 'л'},
    {'name': 'Кола', 'category': 'Напитки', 'price': 95.00, 'quantity': 150, 'unit': 'л'},
]

for product_data in products_data:
    category_name = product_data.pop('category')
    category = Category.objects.get(name=category_name)
    
    # Добавляем срок годности для некоторых товаров
    expiry_date = None
    if category_name in ['Молочные продукты', 'Мясо и птица', 'Хлебобулочные изделия']:
        expiry_date = timezone.now().date() + timedelta(days=random.randint(5, 30))
    
    product, created = Product.objects.get_or_create(
        name=product_data['name'],
        category=category,
        defaults={
            'price': product_data['price'],
            'quantity': product_data['quantity'],
            'unit': product_data['unit'],
            'expiry_date': expiry_date,
            'description': f'Качественный товар - {product_data["name"]}'
        }
    )
    if created:
        print(f"✓ Создан товар: {product.name} - {product.price} ₽/{product.unit}")

print("\n" + "="*50)
print("✓ Тестовые данные успешно созданы!")
print("="*50)
print("\nДля входа используйте:")
print("\nДиректор:")
print("  Логин: director")
print("  Пароль: director123")
print("\nЗаведующий:")
print("  Логин: manager")
print("  Пароль: manager123")
print("\nКассир:")
print("  Логин: cashier")
print("  Пароль: cashier123")
print("="*50)
