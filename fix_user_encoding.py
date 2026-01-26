# -*- coding: utf-8 -*-
"""
Скрипт для исправления кодировки пользователей в базе данных
"""
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from accounts.models import CustomUser

print('=' * 60)
print('ИСПРАВЛЕНИЕ КОДИРОВКИ ПОЛЬЗОВАТЕЛЕЙ')
print('=' * 60)
print()

# Обновляем всех пользователей с правильной кодировкой
users = CustomUser.objects.all()

print(f'Найдено пользователей: {users.count()}')
print()

for user in users:
    print(f'Пользователь: {user.username}')
    print(f'  Текущее имя: {user.first_name} {user.last_name}')
    
    # Исправляем стандартных пользователей
    if user.username == 'admin':
        user.first_name = 'Админ'
        user.last_name = 'Администратор'
        user.save()
        print(f'  ✓ Обновлено: {user.first_name} {user.last_name}')
    elif user.username == 'manager':
        user.first_name = 'Менеджер'
        user.last_name = 'Иванов'
        user.save()
        print(f'  ✓ Обновлено: {user.first_name} {user.last_name}')
    elif user.username == 'cashier':
        user.first_name = 'Кассир'
        user.last_name = 'Петров'
        user.save()
        print(f'  ✓ Обновлено: {user.first_name} {user.last_name}')
    print()

print('=' * 60)
print('✓ ГОТОВО! Кодировка исправлена.')
print('=' * 60)
print()
print('Перезагрузите страницу в браузере (Ctrl+F5)')
