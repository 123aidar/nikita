from django.contrib import admin
from .models import Category, Product, PriceHistory, Supply, SupplyItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']

from .models import ProductInstance

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'barcode', 'category', 'price', 'quantity', 'unit']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'barcode', 'description']
    date_hierarchy = 'created_at'
    readonly_fields = ['created_at', 'updated_at']

@admin.register(ProductInstance)
class ProductInstanceAdmin(admin.ModelAdmin):
    list_display = ['product', 'serial_number', 'expiry_date', 'is_sold', 'created_at']
    list_filter = ['product', 'expiry_date', 'is_sold']
    search_fields = ['serial_number', 'product__name']

@admin.register(PriceHistory)
class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'old_price', 'new_price', 'changed_at', 'changed_by']
    list_filter = ['changed_at']
    date_hierarchy = 'changed_at'

class SupplyItemInline(admin.TabularInline):
    model = SupplyItem
    extra = 0
    readonly_fields = ['price_per_unit']

@admin.register(Supply)
class SupplyAdmin(admin.ModelAdmin):
    list_display = ['id', 'supplier', 'supply_date', 'total_cost', 'created_by']
    list_filter = ['supply_date', 'supplier']
    search_fields = ['supplier']
    date_hierarchy = 'supply_date'
    readonly_fields = ['total_cost']
    inlines = [SupplyItemInline]

@admin.register(SupplyItem)
class SupplyItemAdmin(admin.ModelAdmin):
    list_display = ['supply', 'product', 'quantity', 'price_per_unit']
    list_filter = ['supply__supply_date']
    search_fields = ['product__name']
