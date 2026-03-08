import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from accounts.models import CustomUser
from products.models import Category, Product
from django.utils import timezone
from datetime import timedelta
import random

print("Создание тестовых данных...")

# Удаление старых данных
CustomUser.objects.all().delete()
Product.objects.all().delete()
Category.objects.all().delete()

# Создание категорий
print("\nСоздание категорий...")

categories_data = [
    ('Овощи и фрукты', 'fa-carrot', 'Свежие овощи и фрукты'),
    ('Молочные продукты', 'fa-cheese', 'Молоко, кефир, сметана, сыр'),
    ('Мясо и птица', 'fa-drumstick-bite', 'Свежее мясо и птица'),
    ('Хлебобулочные изделия', 'fa-bread-slice', 'Хлеб и выпечка'),
    ('Напитки', 'fa-bottle-water', 'Вода, соки, газировка'),
    ('Крупы', 'fa-seedling', 'Крупы и макароны'),
    ('Консервы', 'fa-can-food', 'Консервированные продукты'),
    ('Сладости', 'fa-candy-cane', 'Конфеты, шоколад'),
]

for name, icon, desc in categories_data:
    category = Category.objects.create(name=name, icon=icon, description=desc)
    print(f"✓ Категория: {name}")

# Создание пользователей
print("\nСоздание пользователей...")

manager = CustomUser.objects.create_user(
    username='manager',
    email='manager@store.com',
    password='manager123',
    first_name='Мария',
    last_name='Сидорова',
    role='manager'
)
print("✓ Заведующий: manager / manager123")

cashier = CustomUser.objects.create_user(
    username='cashier',
    email='cashier@store.com',
    password='cashier123',
    first_name='Анна',
    last_name='Иванова',
    role='cashier'
)
print("✓ Кассир: cashier / cashier123")

# Получение категорий
categories = Category.objects.all()

# Создание товаров
print("\nСоздание товаров...")

products_data = [
    # Овощи
    ('Картофель', 'Овощи и фрукты', 35.50, 120),
    ('Морковь', 'Овощи и фрукты', 42.00, 85),
    ('Лук репчатый', 'Овощи и фрукты', 28.00, 95),
    ('Помидоры', 'Овощи и фрукты', 89.00, 65),
    ('Огурцы', 'Овощи и фрукты', 75.00, 70),
    ('Капуста белокочанная', 'Овощи и фрукты', 32.00, 110),
    
    # Фрукты
    ('Яблоки Голден', 'Овощи и фрукты', 95.00, 80),
    ('Бананы', 'Овощи и фрукты', 68.00, 90),
    ('Апельсины', 'Овощи и фрукты', 85.00, 75),
    ('Груши', 'Овощи и фрукты', 105.00, 60),
    
    # Молочные
    ('Молоко 3.2%', 'Молочные продукты', 75.00, 150),
    ('Кефир 2.5%', 'Молочные продукты', 68.00, 120),
    ('Сметана 20%', 'Молочные продукты', 95.00, 80),
    ('Сыр Российский', 'Молочные продукты', 485.00, 45),
    
    # Мясо
    ('Говядина', 'Мясо и птица', 520.00, 35),
    ('Свинина', 'Мясо и птица', 450.00, 40),
    ('Курица', 'Мясо и птица', 285.00, 60),
    
    # Хлеб
    ('Хлеб белый', 'Хлебобулочные изделия', 38.00, 200),
    ('Хлеб черный', 'Хлебобулочные изделия', 42.00, 180),
    ('Батон нарезной', 'Хлебобулочные изделия', 35.00, 150),
    
    # Напитки
    ('Вода минеральная', 'Напитки', 45.00, 200),
    ('Сок апельсиновый', 'Напитки', 95.00, 120),
    ('Кола 1л', 'Напитки', 85.00, 100),
]

for name, cat_name, price, stock in products_data:
    try:
        category = Category.objects.get(name=cat_name)
        product = Product.objects.create(
            name=name,
            category=category,
            price=price,
            quantity=stock,
            description=f'Качественный товар - {name}'
        )
        print(f"✓ {name} - {price} руб.")
    except Exception as e:
        print(f"✗ Ошибка при создании {name}: {e}")

print("\n" + "="*50)
print("Тестовые данные успешно созданы!")
print("="*50)
print("\nДля входа используйте:")
print("\nЗаведующий (полный доступ):")
print("  Логин: manager")
print("  Пароль: manager123")
print("\nКассир:")
print("  Логин: cashier")
print("  Пароль: cashier123")
print("="*50)
