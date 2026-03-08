# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from products.models import Category, Product, Supply, SupplyItem
from django.utils import timezone
import uuid


class Command(BaseCommand):
    help = 'Создать тестовые данные для магазина'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создаём суперпользователя...')
        if not CustomUser.objects.filter(username='admin').exists():
            user = CustomUser.objects.create_superuser(
                'admin', 
                'admin@example.com', 
                'admin123', 
                first_name='Админ', 
                last_name='Системы', 
                phone='+79991234567', 
                role='manager'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Суперпользователь создан: {user}'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ Суперпользователь уже существует'))

        self.stdout.write('\nСоздаём категории...')
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
                self.stdout.write(self.style.SUCCESS(f'✓ Создана категория: {cat.name}'))

        self.stdout.write('\nСоздаём товары...')
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

        for name, cat_name, price, unit in products_data:
            category = Category.objects.filter(name=cat_name).first()
            if not category:
                category = Category.objects.first()
            
            prod, created = Product.objects.get_or_create(
                name=name,
                defaults={
                    'category': category,
                    'price': price,
                    'quantity': 0,
                    'unit': unit,
                    'description': f'Свежий товар: {name}'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Создан товар: {prod.name}'))

        self.stdout.write('\nСоздаём поставку...')
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
            self.stdout.write(self.style.SUCCESS(f'✓ Поставка №{supply.id} создана'))
        else:
            self.stdout.write(self.style.ERROR('✗ Не удалось создать поставку'))

        self.stdout.write(self.style.SUCCESS('\n✓ Все данные созданы успешно!'))
