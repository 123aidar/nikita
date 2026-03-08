# -*- coding: utf-8 -*-
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery_store.settings')
django.setup()

from chat.models import Message

# Получаем количество сообщений до удаления
count = Message.objects.count()

# Удаляем все сообщения
Message.objects.all().delete()

print(f'✓ Удалено сообщений из чата: {count}')
print('✓ История чата полностью очищена!')
