# -*- coding: utf-8 -*-
"""
Скрипт для тестирования функционала штрих-кодов
Используйте: python test_barcode_feature.py
"""

import os
import django
import sys

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from products.models import Product
from decimal import Decimal
import random

def generate_barcode():
    """Generate a unique EAN-13 barcode"""
    base = '200' + ''.join([str(random.randint(0, 9)) for _ in range(9)])
    odd_sum = sum(int(base[i]) for i in range(0, 12, 2))
    even_sum = sum(int(base[i]) for i in range(1, 12, 2))
    check_digit = (10 - ((odd_sum + even_sum * 3) % 10)) % 10
    return base + str(check_digit)

def test_barcodes():
    """Тест функционала штрих-кодов"""
    
    print("=" * 70)
    print("ТЕСТИРОВАНИЕ ФУНКЦИОНАЛА ШТРИХ-КОДОВ")
    print("=" * 70)
    print()
    
    # 1. Проверка наличия штрих-кодов у товаров
    print("1. Проверка штрих-кодов у товаров:")
    print("-" * 70)
    
    products = Product.objects.all()
    total_products = products.count()
    products_with_barcode = products.exclude(barcode__isnull=True).exclude(barcode='').count()
    
    print(f"   Всего товаров: {total_products}")
    print(f"   С штрих-кодом: {products_with_barcode}")
    print(f"   Без штрих-кода: {total_products - products_with_barcode}")
    print()
    
    if products_with_barcode == 0:
        print("   ⚠️  ВНИМАНИЕ: Нет товаров со штрих-кодами!")
        print("   Запустите: python manage.py generate_barcodes")
        print()
        return
    
    # 2. Показать несколько примеров
    print("2. Примеры товаров со штрих-кодами:")
    print("-" * 70)
    
    sample_products = products.exclude(barcode__isnull=True).exclude(barcode='')[:5]
    for product in sample_products:
        price_with_markup = product.price * Decimal('1.38')
        print(f"   📦 {product.name[:40]:<40}")
        print(f"      Штрих-код: {product.barcode}")
        print(f"      Цена: {product.price} руб. ({price_with_markup:.2f} руб. с наценкой)")
        print(f"      Остаток: {product.quantity} {product.unit}")
        print()
    
    # 3. Тест поиска по штрих-коду
    print("3. Тест поиска по штрих-коду:")
    print("-" * 70)
    
    test_product = sample_products[0] if sample_products else None
    if test_product:
        print(f"   Ищем товар с кодом: {test_product.barcode}")
        found = Product.objects.filter(barcode=test_product.barcode).first()
        if found:
            print(f"   ✓ Найдено: {found.name}")
            print(f"   ✓ ID: {found.id}")
            print(f"   ✓ Цена: {found.price} руб.")
        else:
            print(f"   ✗ Не найдено!")
    print()
    
    # 4. Проверка уникальности штрих-кодов
    print("4. Проверка уникальности штрих-кодов:")
    print("-" * 70)
    
    from django.db.models import Count
    duplicates = Product.objects.values('barcode').annotate(
        count=Count('barcode')
    ).filter(count__gt=1).exclude(barcode__isnull=True).exclude(barcode='')
    
    if duplicates.exists():
        print(f"   ✗ Найдено дубликатов: {duplicates.count()}")
        for dup in duplicates:
            print(f"      Штрих-код {dup['barcode']} используется {dup['count']} раз")
    else:
        print(f"   ✓ Все штрих-коды уникальны!")
    print()
    
    # 5. Информация об API
    print("5. Доступные API endpoints:")
    print("-" * 70)
    print("   GET /sales/api/search-barcode/?barcode=<код>")
    print("      - Поиск товара по штрих-коду для формы продажи")
    print()
    print("   GET /products/<id>/barcode-image/")
    print("      - Получить изображение штрих-кода в формате PNG")
    print()
    print("   GET /products/<id>/barcode-label/")
    print("      - Страница печати этикетки со штрих-кодом")
    print()
    
    # 6. Инструкция по использованию
    print("6. Как использовать:")
    print("-" * 70)
    print("   1. Откройте форму создания продажи: /sales/create/")
    print("   2. В верхней части найдите поле 'Сканер штрих-кодов'")
    print("   3. Наведите сканер на штрих-код товара")
    print("   4. Или введите вручную, например:")
    if test_product:
        print(f"      {test_product.barcode}")
    print("   5. Товар автоматически добавится в список")
    print()
    
    # 7. Статистика
    print("7. Статистика:")
    print("-" * 70)
    if test_product:
        print(f"   Для быстрого теста используйте:")
        print(f"   URL: http://localhost:8000/sales/api/search-barcode/?barcode={test_product.barcode}")
        print()
        print(f"   Или откройте в браузере:")
        print(f"   http://localhost:8000/products/{test_product.id}/barcode-label/")
    print()
    
    print("=" * 70)
    print("✓ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО")
    print("=" * 70)
    print()
    print("Для генерации штрих-кодов используйте:")
    print("  python manage.py generate_barcodes")
    print()
    print("Для перегенерации всех штрих-кодов:")
    print("  python manage.py generate_barcodes --regenerate")
    print()

if __name__ == '__main__':
    try:
        test_barcodes()
    except Exception as e:
        print(f"Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
