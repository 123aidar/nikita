# -*- coding: utf-8 -*-
"""
Management command to generate barcodes for products
"""
from django.core.management.base import BaseCommand
from products.models import Product
import random


class Command(BaseCommand):
    help = 'Генерирует штрих-коды для товаров без штрих-кода'

    def add_arguments(self, parser):
        parser.add_argument(
            '--regenerate',
            action='store_true',
            help='Перегенерировать штрих-коды для всех товаров',
        )

    def generate_barcode(self):
        """Generate a unique EAN-13 barcode starting with 200 (internal use)"""
        # EAN-13 format: 12 digits + 1 check digit
        # Start with 200-299 for internal barcodes
        base = '200' + ''.join([str(random.randint(0, 9)) for _ in range(9)])
        
        # Calculate EAN-13 check digit
        odd_sum = sum(int(base[i]) for i in range(0, 12, 2))
        even_sum = sum(int(base[i]) for i in range(1, 12, 2))
        check_digit = (10 - ((odd_sum + even_sum * 3) % 10)) % 10
        
        return base + str(check_digit)

    def handle(self, *args, **options):
        regenerate = options['regenerate']
        
        if regenerate:
            products = Product.objects.all()
            self.stdout.write(self.style.WARNING(
                f'Регенерация штрих-кодов для всех {products.count()} товаров...'
            ))
        else:
            products = Product.objects.filter(barcode__isnull=True) | Product.objects.filter(barcode='')
            if not products.exists():
                self.stdout.write(self.style.SUCCESS(
                    '✓ Все товары уже имеют штрих-коды!'
                ))
                return
            
            self.stdout.write(self.style.WARNING(
                f'Генерация штрих-кодов для {products.count()} товаров...'
            ))
        
        generated = 0
        existing_barcodes = set(Product.objects.exclude(
            barcode__isnull=True
        ).exclude(
            barcode=''
        ).values_list('barcode', flat=True))
        
        for product in products:
            # Generate unique barcode
            barcode = self.generate_barcode()
            attempts = 0
            while barcode in existing_barcodes and attempts < 100:
                barcode = self.generate_barcode()
                attempts += 1
            
            if attempts >= 100:
                self.stdout.write(self.style.ERROR(
                    f'✗ Не удалось сгенерировать уникальный штрих-код для "{product.name}"'
                ))
                continue
            
            product.barcode = barcode
            product.save()
            existing_barcodes.add(barcode)
            generated += 1
            
            self.stdout.write(self.style.SUCCESS(
                f'✓ {product.name}: {barcode}'
            ))
        
        self.stdout.write(self.style.SUCCESS(
            f'\n✓ Успешно сгенерировано {generated} штрих-кодов!'
        ))
