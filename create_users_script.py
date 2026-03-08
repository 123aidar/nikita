#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Скрипт для создания пользователей магазина "На Просторной"
Запуск: python create_users_script.py
"""

import os
import sys
import django

# Настройка Django окружения
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from accounts.models import CustomUser


def create_users():
    """Создает пользователей с разными ролями"""
    
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

    print('\n' + '='*70)
    print('  Создание пользователей магазина "На Просторной"')
    print('='*70 + '\n')

    created = []
    skipped = []

    for user_data in users_data:
        username = user_data['username']
        
        if CustomUser.objects.filter(username=username).exists():
            print(f'⚠  Пользователь "{username}" уже существует - пропущен')
            skipped.append(username)
            continue

        password = user_data.pop('password')
        user = CustomUser.objects.create(**user_data)
        user.set_password(password)
        user.save()
        
        print(f'✓  Создан: {user.get_full_name()} ({user.get_role_display()})')
        created.append({'user': user, 'password': password})

    # Итоги
    print('\n' + '-'*70)
    print(f'Создано пользователей: {len(created)}')
    if skipped:
        print(f'Пропущено (уже существуют): {len(skipped)}')
    print('-'*70)

    # Учетные данные
    if created:
        print('\n' + '='*70)
        print('  УЧЕТНЫЕ ДАННЫЕ ДЛЯ ВХОДА')
        print('='*70)
        
        for item in created:
            user = item['user']
            password = item['password']
            print(f'\n{user.get_role_display()}:')
            print(f'  Логин:    {user.username}')
            print(f'  Пароль:   {password}')
            print(f'  Email:    {user.email}')
        
        print('\n' + '='*70)
        print('⚠  ВАЖНО: Сохраните эти данные и смените пароли после первого входа!')
        print('='*70 + '\n')
    
    return len(created), len(skipped)


if __name__ == '__main__':
    try:
        created_count, skipped_count = create_users()
        
        if created_count > 0:
            print('\n✓ Пользователи успешно созданы!')
            print(f'  URL для входа: http://127.0.0.1:8080/accounts/login/')
        elif skipped_count > 0:
            print('\n→ Все пользователи уже существуют в системе')
        
        sys.exit(0)
        
    except Exception as e:
        print(f'\n✗ Ошибка при создании пользователей: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)
