from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Sum, F
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta
from .models import Product, Category, Supply, SupplyItem, PriceHistory
from django.db.models import Q
from .forms import ProductForm, PriceUpdateForm, CategoryForm
import json

@login_required
def dashboard(request):
    total_products = Product.objects.count()
    low_stock_products = Product.objects.filter(quantity__lt=10).count()
    from .models import ProductInstance
    expired_products = ProductInstance.objects.filter(expiry_date__lt=timezone.now().date(), is_sold=False).count()
    categories = Category.objects.all()
    
    # Получаем последние добавленные товары
    recent_products = Product.objects.all()[:8]
    
    context = {
        'total_products': total_products,
        'low_stock_products': low_stock_products,
        'expired_products': expired_products,
        'categories': categories,
        'recent_products': recent_products,
    }
    return render(request, 'products/dashboard.html', context)

@login_required
def product_list(request):
    # Показываем только категории
    categories = Category.objects.all()
    
    # Добавляем количество товаров в каждой категории
    for category in categories:
        category.product_count = Product.objects.filter(category=category).count()
    
    context = {
        'categories': categories,
    }
    return render(request, 'products/product_list.html', context)

@login_required
@user_passes_test(lambda u: u.can_manage_products())
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Категория "{category.name}" успешно создана!')
            return redirect('products:product_list')
    else:
        form = CategoryForm()
    
    context = {
        'form': form,
        'title': 'Создание категории',
    }
    return render(request, 'products/category_form.html', context)

@login_required
@user_passes_test(lambda u: u.can_manage_products())
def category_update(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Категория "{category.name}" успешно обновлена!')
            return redirect('products:category_products', category_id=category.id)
    else:
        form = CategoryForm(instance=category)
    
    context = {
        'form': form,
        'title': 'Редактирование категории',
        'category': category,
    }
    return render(request, 'products/category_form.html', context)

@login_required
@user_passes_test(lambda u: u.can_manage_products())
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Категория "{category_name}" успешно удалена!')
        return redirect('products:product_list')
    return redirect('products:category_products', category_id=category_id)

@login_required
def category_products(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    search_query = request.GET.get('search', '')

    products = Product.objects.filter(category=category)

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(sku__icontains=search_query)
        ).distinct()

    context = {
        'category': category,
        'products': products,
        'search_query': search_query,
    }
    return render(request, 'products/category_products.html', context)

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    price_history = product.price_history.all()[:10]
    # Получаем поставки через SupplyItem
    supply_items = product.supply_items.select_related('supply').order_by('-supply__supply_date')[:10]
    instances = product.instances.all()

    context = {
        'product': product,
        'price_history': price_history,
        'supply_items': supply_items,
        'instances': instances,
    }
    return render(request, 'products/product_detail.html', context)

@login_required
def product_create(request):
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('products:product_list')
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Товар успешно добавлен!')
            return redirect('products:product_list')
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Добавить товар'})

@login_required
def product_update(request, pk):
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('products:product_list')
    
    product = get_object_or_404(Product, pk=pk)
    old_sku = product.sku  # Сохраняем старый артикул
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            updated_product = form.save(commit=False)
            # Восстанавливаем артикул, чтобы он не был удален
            if old_sku:
                updated_product.sku = old_sku
            updated_product.save()
            messages.success(request, 'Товар успешно обновлен!')
            return redirect('products:product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {'form': form, 'title': 'Редактировать товар', 'product': product})

@login_required
@user_passes_test(lambda u: u.can_manage_products())
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        category_id = product.category.id
        product_name = product.name
        product.delete()
        messages.success(request, f'Товар "{product_name}" успешно удален!')
        return redirect('products:category_products', category_id=category_id)
    return redirect('products:product_detail', pk=pk)

@login_required
def supply_list(request):
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('products:dashboard')
    
    supplies = Supply.objects.all()
    return render(request, 'products/supply_list.html', {'supplies': supplies})

@login_required
def supply_create(request):
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('products:dashboard')
    
    if request.method == 'POST':
        try:
            # Получаем данные из формы
            items_data = json.loads(request.POST.get('items_data', '[]'))
            supplier = request.POST.get('supplier', '')
            notes = request.POST.get('notes', '')
            
            if not items_data:
                messages.error(request, 'Добавьте хотя бы один товар в поставку!')
                products = Product.objects.all().order_by('name')
                return render(request, 'products/supply_form.html', {'products': products})
            
            if not supplier:
                messages.error(request, 'Укажите поставщика!')
                products = Product.objects.all().order_by('name')
                return render(request, 'products/supply_form.html', {'products': products})
            
            # Создаем поставку
            supply = Supply.objects.create(
                supplier=supplier,
                created_by=request.user,
                notes=notes
            )
            
            # Добавляем позиции
            for item in items_data:
                product = Product.objects.get(id=item['product_id'])
                price = float(item.get('price', product.price))
                SupplyItem.objects.create(
                    supply=supply,
                    product=product,
                    quantity=float(item['quantity']),
                    price_per_unit=price
                )
            
            messages.success(request, f'Поставка №{supply.id} успешно зарегистрирована на сумму {supply.total_cost} руб.!')
            return redirect('products:supply_list')
            
        except Exception as e:
            messages.error(request, f'Ошибка при создании поставки: {str(e)}')
            products = Product.objects.all().order_by('name')
            return render(request, 'products/supply_form.html', {'products': products})
    else:
        products = Product.objects.all().order_by('name')
        return render(request, 'products/supply_form.html', {'products': products})

@login_required
def price_update(request, pk):
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для выполнения этого действия.')
        return redirect('products:product_list')
    
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = PriceUpdateForm(request.POST)
        if form.is_valid():
            new_price = form.cleaned_data['new_price']
            
            # Сохраняем историю изменения цены
            PriceHistory.objects.create(
                product=product,
                old_price=product.price,
                new_price=new_price,
                changed_by=request.user
            )
            
            # Обновляем цену товара
            product.price = new_price
            product.save()
            
            messages.success(request, f'Цена товара "{product.name}" успешно обновлена!')
            return redirect('products:product_detail', pk=pk)
    else:
        form = PriceUpdateForm(initial={'new_price': product.price})
    
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'products/price_update.html', context)


@login_required
def print_supply_invoice(request, supply_id):
    if not request.user.can_manage_products():
        messages.error(request, 'У вас нет прав для просмотра накладных.')
        return redirect('products:supply_list')
    
    supply = get_object_or_404(Supply, id=supply_id)
    supply_items = SupplyItem.objects.filter(supply=supply).select_related('product__category')
    
    context = {
        'supply': supply,
        'supply_items': supply_items,
    }
    return render(request, 'products/supply_invoice.html', context)
