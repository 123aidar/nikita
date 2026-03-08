# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from accounts.models import CustomUser

# Удаляем старого админа если есть
CustomUser.objects.filter(username='admin').delete()

# Создаем нового с правильной кодировкой
admin = CustomUser.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin',
    first_name='Админ',
    last_name='Администратор',
    phone='+79991234567',
    role='manager'
)

print(f'✓ Суперпользователь создан: {admin.get_full_name()}')
print(f'  Логин: admin')
print(f'  Пароль: admin')
