# -*- coding: utf-8 -*-
"""
Принудительный сброс и пересоздание базы данных.
Используется один раз для исправления данных.
"""
import os
import sys
import django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Category, Product

User = get_user_model()

print('=' * 60)
print('ПРИНУДИТЕЛЬНЫЙ СБРОС БАЗЫ ДАННЫХ')
print('=' * 60)

# Удаляем все данные
deleted_products = Product.objects.all().delete()
deleted_categories = Category.objects.all().delete()
deleted_users = User.objects.all().delete()

print(f'Удалено товаров: {deleted_products[0]}')
print(f'Удалено категорий: {deleted_categories[0]}')
print(f'Удалено пользователей: {deleted_users[0]}')

print('\nЗапускаем инициализацию...\n')

# Запускаем init_data.py
import init_data
init_data.init_database()
