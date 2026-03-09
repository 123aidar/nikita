# -*- coding: utf-8 -*-
"""
Django management command для добавления расширенного каталога товаров
Использование: python manage.py load_products
"""
from django.core.management.base import BaseCommand
from products.models import Category, Product
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Загружает расширенный каталог товаров в базу данных'

    def handle(self, *args, **options):
        self.stdout.write('=' * 60)
        self.stdout.write('ЗАГРУЗКА РАСШИРЕННОГО КАТАЛОГА ТОВАРОВ')
        self.stdout.write('=' * 60)
        
        # Импортируем данные из add_many_products.py
        import sys
        import os
        sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        
        from add_many_products import products_data
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        bulk_products = []
        
        for category_name, products in products_data.items():
            try:
                category = Category.objects.get(name=category_name)
                self.stdout.write(f'\nКатегория: {category_name}')
                
                # Получаем существующие товары
                existing_products = set(
                    Product.objects.filter(category=category).values_list('name', flat=True)
                )
                
                for name, unit, purchase_price, selling_price in products:
                    if name in existing_products:
                        skipped_count += 1
                        continue
                    
                    quantity = random.randint(15, 200)
                    
                    bulk_products.append(Product(
                        name=name,
                        category=category,
                        description=f'Качественный товар из категории {category_name}',
                        price=Decimal(str(selling_price)),
                        quantity=quantity,
                        unit=unit
                    ))
                    
                    created_count += 1
                    
            except Category.DoesNotExist:
                self.stdout.write(self.style.WARNING(f'Категория "{category_name}" не найдена'))
                continue
        
        # Массовая вставка
        if bulk_products:
            Product.objects.bulk_create(bulk_products, batch_size=100)
            self.stdout.write(self.style.SUCCESS(f'\n{"="*60}'))
            self.stdout.write(self.style.SUCCESS(f'Создано товаров: {created_count}'))
            self.stdout.write(self.style.SUCCESS(f'Пропущено существующих: {skipped_count}'))
            self.stdout.write(self.style.SUCCESS(f'Всего товаров в БД: {Product.objects.count()}'))
            self.stdout.write(self.style.SUCCESS(f'{"="*60}'))
        else:
            self.stdout.write(self.style.WARNING('Все товары уже существуют'))
