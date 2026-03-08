"""
Management команда для создания пользователей с разными ролями
Использование: python manage.py create_users
"""
from django.core.management.base import BaseCommand
from accounts.models import CustomUser


class Command(BaseCommand):
    help = 'Создает пользователей: менеджер и кассир'

    def handle(self, *args, **options):
        users_data = [
            {
                'username': 'manager',
                'password': 'manager123',
                'email': 'manager@prostornaya.ru',
                'first_name': 'Мария',
                'last_name': 'Менеджерова',
                'role': 'manager',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'cashier',
                'password': 'cashier123',
                'email': 'cashier@prostornaya.ru',
                'first_name': 'Анна',
                'last_name': 'Кассирова',
                'role': 'cashier',
                'is_staff': False,
                'is_superuser': False,
            },
        ]

        created_count = 0
        skipped_count = 0

        self.stdout.write('\n' + '='*60)
        self.stdout.write(self.style.SUCCESS('Создание пользователей магазина "На Просторной"'))
        self.stdout.write('='*60 + '\n')

        for user_data in users_data:
            username = user_data['username']
            
            if CustomUser.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠ Пользователь "{username}" уже существует - пропущен')
                )
                skipped_count += 1
                continue

            # Извлекаем пароль отдельно
            password = user_data.pop('password')
            
            # Создаем пользователя
            user = CustomUser.objects.create(**user_data)
            user.set_password(password)
            user.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'✓ Создан: {user.get_full_name()} '
                    f'(Логин: {user.username}, Роль: {user.get_role_display()})'
                )
            )
            created_count += 1

        # Итоговая информация
        self.stdout.write('\n' + '-'*60)
        self.stdout.write(self.style.SUCCESS(f'Создано пользователей: {created_count}'))
        if skipped_count > 0:
            self.stdout.write(self.style.WARNING(f'Пропущено (уже существуют): {skipped_count}'))
        self.stdout.write('-'*60)

        if created_count > 0:
            self.stdout.write('\n' + self.style.SUCCESS('УЧЕТНЫЕ ДАННЫЕ ДЛЯ ВХОДА:'))
            self.stdout.write('='*60)
            
            for user_data in users_data:
                username = user_data['username']
                user = CustomUser.objects.get(username=username)
                # Восстанавливаем пароль из исходных данных
                password = 'manager123' if username == 'manager' else 'cashier123'
                
                self.stdout.write(
                    f'\n{user.get_role_display()}:\n'
                    f'  Логин:    {username}\n'
                    f'  Пароль:   {password}\n'
                    f'  Email:    {user.email}\n'
                )
            
            self.stdout.write('='*60)
            self.stdout.write(
                self.style.WARNING(
                    '\n⚠ ВАЖНО: Сохраните эти данные и смените пароли после первого входа!\n'
                )
            )
