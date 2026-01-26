from django.contrib import admin
from .models import Sale, SaleItem

class SaleItemInline(admin.TabularInline):
    model = SaleItem
    extra = 0
    readonly_fields = ['price_per_unit']

@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ['id', 'sale_date', 'cashier', 'total_amount']
    list_filter = ['sale_date', 'cashier']
    date_hierarchy = 'sale_date'
    readonly_fields = ['total_amount']
    inlines = [SaleItemInline]

@admin.register(SaleItem)
class SaleItemAdmin(admin.ModelAdmin):
    list_display = ['sale', 'product', 'quantity', 'price_per_unit']
    list_filter = ['sale__sale_date']
    search_fields = ['product__name']
