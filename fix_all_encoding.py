# -*- coding: utf-8 -*-
"""
Скрипт для исправления кодировки всех данных в базе
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from accounts.models import CustomUser
from products.models import Category, Product

print('=' * 70)
print('ИСПРАВЛЕНИЕ КОДИРОВКИ ВСЕХ ДАННЫХ')
print('=' * 70)
print()

# 1. Категории
print('[1] Исправление категорий...')
categories_fix = {
    'РћРІРѕС‰Рё': 'Овощи',
    'Р¤СЂСѓРєС‚С‹': 'Фрукты',
    'РњРѕР»РѕС‡РЅС‹Рµ': 'Молочные продукты',
    'РҐР»РµР±': 'Хлеб и выпечка',
    'РњСЏСЃРѕ': 'Мясо и птица',
    'Р РµРїР°СЃРё': 'Рыба',
    'РќР°РїРёС‚РєРё': 'Напитки'
}

for old_name, new_name in categories_fix.items():
    cats = Category.objects.filter(name__contains='Р')
    for cat in cats:
        if any(char in cat.name for char in ['Р', 'С']):
            # Пытаемся определить правильное имя по первым буквам
            if 'РћРІРѕ' in cat.name or 'Ovo' in cat.name:
                cat.name = 'Овощи'
            elif 'Р¤СЂСѓ' in cat.name or 'Fru' in cat.name:
                cat.name = 'Фрукты'
            elif 'РњРѕР»' in cat.name or 'Mol' in cat.name:
                cat.name = 'Молочные продукты'
            elif 'РҐР»Рµ' in cat.name or 'Hle' in cat.name:
                cat.name = 'Хлеб и выпечка'
            elif 'РњСЏСЃ' in cat.name or 'Myas' in cat.name:
                cat.name = 'Мясо и птица'
            elif 'Р РµРї' in cat.name or 'Rep' in cat.name:
                cat.name = 'Рыба'
            elif 'РќР°Рї' in cat.name or 'Nap' in cat.name:
                cat.name = 'Напитки'
            
            cat.save()
            print(f'  ✓ {cat.name}')

# Создаем заново если нужно
categories_data = [
    ('Овощи', 'fa-carrot'),
    ('Фрукты', 'fa-apple-alt'),
    ('Молочные продукты', 'fa-cheese'),
    ('Хлеб и выпечка', 'fa-bread-slice'),
    ('Мясо и птица', 'fa-drumstick-bite'),
    ('Рыба', 'fa-fish'),
    ('Напитки', 'fa-glass-water')
]

for name, icon in categories_data:
    cat, created = Category.objects.get_or_create(
        name=name,
        defaults={'icon': icon}
    )
    if created:
        print(f'  ✓ Создана: {name}')
    else:
        cat.icon = icon
        cat.save()
        print(f'  ✓ Обновлена: {name}')

print()

# 2. Продукты - проверяем на кракозябры
print('[2] Проверка продуктов...')

products = Product.objects.all()
fixed_count = 0
bad_products = []

for product in products:
    # Проверяем наличие кракозябр (латиница Р или С в русском тексте)
    if 'Р' in product.name or 'С' in product.name:
        bad_products.append(product)
        print(f'  ⚠ Проблема: {product.name} (ID: {product.id})')
        fixed_count += 1

if fixed_count > 0:
    print(f'\n  Найдено {fixed_count} продуктов с проблемами кодировки')
    print('  Рекомендация: запустите full_reset_and_start.bat для пересоздания данных')
else:
    print('  ✓ Все продукты в порядке')

print()
print('=' * 70)
print('✓ ГОТОВО!')
print('=' * 70)
print()
print('ВАЖНО: Перезагрузите страницу в браузере (Ctrl+F5 или Ctrl+Shift+R)')
