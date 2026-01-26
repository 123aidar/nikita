from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from .models import Sale, SaleItem
from products.models import Product
import json

@login_required
def sale_list(request):
    if not request.user.can_manage_sales():
        messages.error(request, 'У вас нет прав для просмотра продаж.')
        return redirect('products:dashboard')
    
    # Фильтры
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    sales = Sale.objects.all()
    
    if date_from:
        sales = sales.filter(sale_date__gte=date_from)
    if date_to:
        sales = sales.filter(sale_date__lte=date_to)
    
    # Статистика
    total_sales = sales.aggregate(total=Sum('total_amount'))['total'] or 0
    total_count = sales.count()
    
    context = {
        'sales': sales,
        'total_sales': total_sales,
        'total_count': total_count,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'sales/sale_list.html', context)

@login_required
def sale_create(request):
    if not request.user.can_manage_sales():
        messages.error(request, 'У вас нет прав для регистрации продаж.')
        return redirect('products:dashboard')
    
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            items_data = json.loads(request.POST.get('items_data', '[]'))
            notes = request.POST.get('notes', '')
            
            if not items_data:
                messages.error(request, 'Добавьте хотя бы один товар в продажу!')
                products = Product.objects.filter(quantity__gt=0).order_by('name')
                return render(request, 'sales/sale_form.html', {'products': products})
            
            # Проверяем наличие всех товаров
            for item in items_data:
                product = Product.objects.get(id=item['product_id'])
                quantity = float(item['quantity'])
                if product.quantity < quantity:
                    messages.error(request, f'Недостаточно товара "{product.name}" на складе! Доступно: {product.quantity} {product.unit}')
                    products = Product.objects.filter(quantity__gt=0).order_by('name')
                    return render(request, 'sales/sale_form.html', {'products': products})
            
            # Создаем продажу
            sale = Sale.objects.create(
                cashier=request.user,
                notes=notes
            )
            
            # Добавляем позиции (цена с наценкой 15% и НДС 20%)
            for item in items_data:
                product = Product.objects.get(id=item['product_id'])
                from decimal import Decimal
                SaleItem.objects.create(
                    sale=sale,
                    product=product,
                    quantity=float(item['quantity']),
                    price_per_unit=product.price * Decimal('1.38')  # 1.15 * 1.2 = 1.38 (+15% наценка +20% НДС)
                )
            
            messages.success(request, f'Продажа №{sale.id} успешно зарегистрирована на сумму {sale.total_amount} руб.!')
            return redirect('sales:sale_list')
            
        except Exception as e:
            messages.error(request, f'Ошибка при создании продажи: {str(e)}')
            products = Product.objects.filter(quantity__gt=0).order_by('name')
            return render(request, 'sales/sale_form.html', {'products': products})
    else:
        products = Product.objects.filter(quantity__gt=0).order_by('name')
        return render(request, 'sales/sale_form.html', {'products': products})

@login_required
def sale_detail(request, pk):
    if not request.user.can_manage_sales():
        messages.error(request, 'У вас нет прав для просмотра продаж.')
        return redirect('products:dashboard')
    
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/sale_detail.html', {'sale': sale})

@login_required
def get_product_info(request, product_id):
    """API для получения информации о товаре (цена, остаток)"""
    try:
        from decimal import Decimal
        product = Product.objects.get(id=product_id)
        # Возвращаем цену с наценкой 15% и НДС 20%
        return JsonResponse({
            'success': True,
            'price': float(product.price * Decimal('1.38')),  # 1.15 * 1.2 = 1.38
            'quantity': float(product.quantity),
            'unit': product.unit
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Товар не найден'
        })

@login_required
def print_receipt(request, pk):
    """Печать чека продажи"""
    if not request.user.can_manage_sales():
        messages.error(request, 'У вас нет прав для просмотра продаж.')
        return redirect('products:dashboard')
    
    sale = get_object_or_404(Sale, pk=pk)
    return render(request, 'sales/receipt.html', {'sale': sale})
