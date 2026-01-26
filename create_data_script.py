# -*- coding: utf-8 -*-
from accounts.models import CustomUser
from products.models import Category, Product, Supply, SupplyItem
from django.utils import timezone

print("Создаём суперпользователя...")
if not CustomUser.objects.filter(username='admin').exists():
    user = CustomUser.objects.create_superuser(
        'admin', 
        'admin@example.com', 
        'admin123', 
        first_name='Админ', 
        last_name='Системы', 
        phone='+79991234567', 
        role='director'
    )
    print(f"✓ Суперпользователь создан: {user}")
else:
    print("✓ Суперпользователь уже существует")

print("\nСоздаём категории...")
categories_data = [
    ('Овощи', 'fa-carrot'),
    ('Фрукты', 'fa-apple-alt'),
    ('Молочные продукты', 'fa-cheese'),
    ('Мясо и птица', 'fa-drumstick-bite'),
    ('Хлебобулочные изделия', 'fa-bread-slice'),
    ('Напитки', 'fa-wine-bottle'),
    ('Крупы', 'fa-box'),
    ('Консервы', 'fa-fish'),
]
for name, icon in categories_data:
    cat, created = Category.objects.get_or_create(name=name, defaults={'icon': icon})
    if created:
        print(f"✓ Создана категория: {cat.name}")
    else:
        print(f"✓ Категория уже существует: {cat.name}")

print("\nСоздаём товары...")
categories = list(Category.objects.all())
products_data = [
    ('Помидоры', 'Овощи', 150.00, 'кг'),
    ('Огурцы', 'Овощи', 120.00, 'кг'),
    ('Яблоки', 'Фрукты', 180.00, 'кг'),
    ('Бананы', 'Фрукты', 100.00, 'кг'),
    ('Молоко', 'Молочные продукты', 80.00, 'л'),
    ('Сыр', 'Молочные продукты', 450.00, 'кг'),
    ('Курица', 'Мясо и птица', 320.00, 'кг'),
    ('Хлеб белый', 'Хлебобулочные изделия', 50.00, 'шт'),
    ('Батон', 'Хлебобулочные изделия', 45.00, 'шт'),
    ('Сок апельсиновый', 'Напитки', 120.00, 'л'),
]

# Сначала создаём товары с временными артикулами
import uuid
for name, cat_name, price, unit in products_data:
    category = Category.objects.filter(name=cat_name).first() or categories[0]
    # Используем временный артикул - он будет заменен при первой поставке
    temp_sku = f"TEMP-{uuid.uuid4().hex[:8].upper()}"
    prod, created = Product.objects.get_or_create(
        name=name,
        defaults={
            'category': category,
            'price': price,
            'quantity': 0,
            'unit': unit,
            'sku': temp_sku,
            'description': f'Свежий товар: {name}'
        }
    )
    if created:
        print(f"✓ Создан товар: {prod.name} (временный артикул: {temp_sku})")

print("\nСоздаём поставку с автоматической генерацией артикулов...")
user = CustomUser.objects.first()
if user and Product.objects.exists():
    supply = Supply.objects.create(
        supplier='ООО "Поставщик"',
        supply_date=timezone.now(),
        created_by=user
    )
    for product in Product.objects.all():
        SupplyItem.objects.create(
            supply=supply,
            product=product,
            quantity=50,
            price_per_unit=product.price
        )
    supply.calculate_total()
    print(f"✓ Поставка №{supply.id} создана, артикулы присвоены автоматически")
    
    # Выводим созданные артикулы
    print("\nАртикулы товаров:")
    for product in Product.objects.all():
        print(f"  {product.name}: {product.sku}")
else:
    print("✗ Не удалось создать поставку (нет пользователя или товаров)")

print("\n✓ Все данные созданы успешно!")
