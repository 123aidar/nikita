# -*- coding: utf-8 -*-
"""
Скрипт для проверки и восстановления артикулов товаров
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from products.models import Product

print('=' * 70)
print('ПРОВЕРКА АРТИКУЛОВ ТОВАРОВ')
print('=' * 70)
print()

products = Product.objects.all()
products_without_sku = []
products_with_sku = []

for product in products:
    if not product.sku:
        products_without_sku.append(product)
        print(f'⚠ ВНИМАНИЕ: У товара "{product.name}" (ID: {product.id}) НЕТ артикула!')
    else:
        products_with_sku.append(product)
        print(f'✓ Товар "{product.name}" (ID: {product.id}) - SKU: {product.sku}')

print()
print('=' * 70)
print(f'Всего товаров: {products.count()}')
print(f'✓ С артикулами: {len(products_with_sku)}')
print(f'⚠ Без артикулов: {len(products_without_sku)}')
print('=' * 70)
print()

if products_without_sku:
    print('ВАЖНО: Товары без артикулов получат их автоматически при следующей поставке.')
    print('       Или вы можете создать поставку для этих товаров.')
else:
    print('✓ ВСЕ ТОВАРЫ ИМЕЮТ АРТИКУЛЫ!')
