from django.contrib import admin
from .models import WriteOff, Inventory

@admin.register(WriteOff)
class WriteOffAdmin(admin.ModelAdmin):
    list_display = ['product', 'quantity', 'reason', 'write_off_date', 'created_by']
    list_filter = ['reason', 'write_off_date']
    search_fields = ['product__name']
    date_hierarchy = 'write_off_date'

@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = ['product', 'expected_quantity', 'actual_quantity', 'difference', 'inventory_date', 'conducted_by']
    list_filter = ['inventory_date']
    search_fields = ['product__name']
    date_hierarchy = 'inventory_date'
    readonly_fields = ['difference']
