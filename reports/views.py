from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import timedelta
from sales.models import Sale
from products.models import Product
from inventory.models import WriteOff
from accounts.models import CustomUser

@login_required
def reports_dashboard(request):
    if not request.user.can_view_reports():
        from django.contrib import messages
        messages.error(request, 'У вас нет прав для просмотра отчетов.')
        from django.shortcuts import redirect
        return redirect('products:dashboard')
    
    return render(request, 'reports/dashboard.html')

@login_required
def profit_chart_data(request):
    if not request.user.can_view_reports():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    period = request.GET.get('period', 'week')  # week, month, year
    
    # Определяем период
    today = timezone.now().date()
    if period == 'week':
        start_date = today - timedelta(days=7)
        date_format = '%d.%m'
    elif period == 'month':
        start_date = today - timedelta(days=30)
        date_format = '%d.%m'
    else:  # year
        start_date = today - timedelta(days=365)
        date_format = '%m.%Y'
    
    # Получаем продажи за период
    sales = Sale.objects.filter(sale_date__gte=start_date).extra(
        select={'date': "DATE(sale_date)"}
    ).values('date').annotate(
        total=Sum('total_amount')
    ).order_by('date')
    
    labels = []
    data = []
    
    for sale in sales:
        date_obj = sale['date']
        if isinstance(date_obj, str):
            from datetime import datetime
            date_obj = datetime.strptime(date_obj, '%Y-%m-%d').date()
        
        labels.append(date_obj.strftime(date_format))
        data.append(float(sale['total']))
    
    return JsonResponse({
        'labels': labels,
        'data': data,
        'period': period
    })

@login_required
def top_products_data(request):
    if not request.user.can_view_reports():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    from sales.models import SaleItem
    
    period = request.GET.get('period', 'week')
    
    today = timezone.now().date()
    if period == 'week':
        start_date = today - timedelta(days=7)
    elif period == 'month':
        start_date = today - timedelta(days=30)
    else:  # year
        start_date = today - timedelta(days=365)
    
    # Получаем топ-10 самых продаваемых товаров
    top_products = SaleItem.objects.filter(
        sale__sale_date__gte=start_date
    ).values(
        'product__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_amount=Sum(F('quantity') * F('price_per_unit'))
    ).order_by('-total_amount')[:10]
    
    labels = []
    quantities = []
    amounts = []
    
    for item in top_products:
        labels.append(item['product__name'])
        quantities.append(float(item['total_quantity']))
        amounts.append(float(item['total_amount']))
    
    return JsonResponse({
        'labels': labels,
        'quantities': quantities,
        'amounts': amounts
    })

@login_required
def statistics_data(request):
    if not request.user.can_view_reports():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    from datetime import datetime
    
    now = timezone.now()
    today = now.date()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    # Статистика продаж
    total_sales_today = Sale.objects.filter(
        sale_date__year=today.year,
        sale_date__month=today.month,
        sale_date__day=today.day
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    total_sales_week = Sale.objects.filter(
        sale_date__gte=week_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    total_sales_month = Sale.objects.filter(
        sale_date__gte=month_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Статистика товаров
    low_stock = Product.objects.filter(quantity__lt=10, quantity__gt=0).count()
    out_of_stock = Product.objects.filter(quantity=0).count()
    expired = 0  # Поле expiry_date не существует в модели Product
    
    # Статистика списаний
    write_offs_week = WriteOff.objects.filter(
        write_off_date__gte=week_ago
    ).count()
    
    write_offs_month = WriteOff.objects.filter(
        write_off_date__gte=month_ago
    ).count()
    
    write_offs_year = WriteOff.objects.filter(
        write_off_date__year=now.year
    ).count()
    
    return JsonResponse({
        'sales': {
            'today': float(total_sales_today),
            'week': float(total_sales_week),
            'month': float(total_sales_month),
        },
        'products': {
            'low_stock': low_stock,
            'out_of_stock': out_of_stock,
            'expired': expired,
        },
        'write_offs': {
            'week': write_offs_week,
            'month': write_offs_month,
            'year': write_offs_year,
        },
    })


@login_required
def detailed_sales_data(request):
    if not request.user.can_view_reports():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        from sales.models import SaleItem
        
        period = request.GET.get('period', 'month')
        now = timezone.now()
        
        if period == 'today':
            start_date = now.replace(hour=0, minute=0, second=0)
        elif period == 'week':
            start_date = now - timedelta(days=7)
        elif period == 'month':
            start_date = now - timedelta(days=30)
        else:
            start_date = now - timedelta(days=365)
        
        sales = Sale.objects.filter(sale_date__gte=start_date).select_related('cashier').order_by('-sale_date')
        
        sales_data = []
        for sale in sales:
            items = SaleItem.objects.filter(sale=sale).select_related('product')
            items_list = [
                {
                    'product': item.product.name,
                    'quantity': float(item.quantity),
                    'price': float(item.price_per_unit),
                    'total': float(item.quantity * item.price_per_unit)
                }
                for item in items
            ]
            
            sales_data.append({
                'date': sale.sale_date.strftime('%d.%m.%Y %H:%M'),
                'sold_by': sale.cashier.get_full_name() if sale.cashier else 'Не указан',
                'total': float(sale.total_amount),
                'items': items_list
            })
        
        return JsonResponse({'sales': sales_data})
    except Exception as e:
        import traceback
        print('Error in detailed_sales_data:', str(e))
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def detailed_products_data(request):
    if not request.user.can_view_reports():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        low_stock_products = Product.objects.filter(quantity__lt=10, quantity__gt=0).select_related('category').order_by('quantity')
        out_of_stock_products = Product.objects.filter(quantity=0).select_related('category')
        
        low_stock_data = [
            {
                'name': p.name,
                'category': p.category.name,
                'quantity': p.quantity,
                'unit': p.unit,
                'price': float(p.price)
            }
            for p in low_stock_products
        ]
        
        out_of_stock_data = [
            {
                'name': p.name,
                'category': p.category.name,
                'price': float(p.price),
                'unit': p.unit
            }
            for p in out_of_stock_products
        ]
        
        return JsonResponse({
            'low_stock': low_stock_data,
            'out_of_stock': out_of_stock_data
        })
    except Exception as e:
        import traceback
        print('Error in detailed_products_data:', str(e))
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def detailed_writeoffs_data(request):
    if not request.user.can_view_reports():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    try:
        period = request.GET.get('period', 'month')
        now = timezone.now()
        
        if period == 'week':
            start_date = now - timedelta(days=7)
        elif period == 'month':
            start_date = now - timedelta(days=30)
        else:  # year
            start_date = now - timedelta(days=365)
        
        writeoffs = WriteOff.objects.filter(
            write_off_date__gte=start_date
        ).select_related('product__category', 'created_by').order_by('-write_off_date')
        
        writeoffs_data = []
        for wo in writeoffs:
            writeoffs_data.append({
                'date': wo.write_off_date.strftime('%d.%m.%Y %H:%M'),
                'product': wo.product.name,
                'category': wo.product.category.name,
                'quantity': float(wo.quantity),
                'unit': wo.product.unit,
                'reason': wo.reason,
                'written_off_by': wo.created_by.get_full_name() if wo.created_by else 'Не указан'
            })
        
        return JsonResponse({'writeoffs': writeoffs_data})
    except Exception as e:
        import traceback
        print('Error in detailed_writeoffs_data:', str(e))
        print(traceback.format_exc())
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def top_sellers_data(request):
    if not request.user.can_view_reports():
        return JsonResponse({'error': 'Access denied'}, status=403)
    
    # Последние 7 дней
    week_ago = timezone.now() - timedelta(days=7)
    
    # Топ продавцов по выручке за неделю
    top_sellers = Sale.objects.filter(
        sale_date__gte=week_ago
    ).values(
        'cashier__first_name', 'cashier__last_name', 'cashier__username'
    ).annotate(
        total_sales=Sum('total_amount'),
        sales_count=Count('id')
    ).order_by('-total_sales')[:5]
    
    sellers_data = []
    for seller in top_sellers:
        full_name = f"{seller['cashier__first_name']} {seller['cashier__last_name']}".strip()
        if not full_name:
            full_name = seller['cashier__username']
        
        sellers_data.append({
            'name': full_name,
            'total_sales': float(seller['total_sales']),
            'sales_count': seller['sales_count'],
            'average_sale': float(seller['total_sales'] / seller['sales_count']) if seller['sales_count'] > 0 else 0
        })
    
    return JsonResponse({'sellers': sellers_data})
