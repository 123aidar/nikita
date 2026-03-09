# -*- coding: utf-8 -*-
"""
Вспомогательный view для загрузки товаров через веб-интерфейс
ТОЛЬКО ДЛЯ АДМИНИСТРАТОРОВ
"""
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.management import call_command
from io import StringIO

@staff_member_required
def load_products_view(request):
    """Страница для загрузки товаров (только для администраторов)"""
    if request.method == 'POST':
        try:
            # Выполняем команду загрузки товаров
            out = StringIO()
            call_command('load_products', stdout=out)
            output = out.getvalue()
            
            messages.success(request, 'Товары успешно загружены!')
            return render(request, 'products/load_products_result.html', {'output': output})
        except Exception as e:
            messages.error(request, f'Ошибка при загрузке товаров: {str(e)}')
    
    from products.models import Product, Category
    context = {
        'total_products': Product.objects.count(),
        'total_categories': Category.objects.count(),
    }
    return render(request, 'products/load_products.html', context)
