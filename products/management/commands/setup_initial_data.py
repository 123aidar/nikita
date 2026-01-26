from django.core.management.base import BaseCommand
from accounts.models import CustomUser
from products.models import Category

class Command(BaseCommand):
    help = 'Создает начальные данные для системы'

    def handle(self, *args, **kwargs):
        self.stdout.write('Создание начальных данных...')
        
        # Создание категорий
        categories = [
            {'name': 'Овощи', 'icon': 'fa-carrot'},
            {'name': 'Фрукты', 'icon': 'fa-apple-alt'},
            {'name': 'Молочные продукты', 'icon': 'fa-cheese'},
            {'name': 'Мясо и птица', 'icon': 'fa-drumstick-bite'},
            {'name': 'Хлебобулочные изделия', 'icon': 'fa-bread-slice'},
            {'name': 'Напитки', 'icon': 'fa-wine-bottle'},
            {'name': 'Крупы', 'icon': 'fa-box'},
            {'name': 'Консервы', 'icon': 'fa-fish'},
        ]
        
        
    from django.core.management.base import BaseCommand

    class Command(BaseCommand):
        help = 'Setup initial data (products, supplies) - очищено для сброса.'

        def handle(self, *args, **kwargs):
            self.stdout.write(self.style.SUCCESS('Initial data setup skipped: all products and supplies must be recreated.'))
