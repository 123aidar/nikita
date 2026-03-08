# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    icon = models.CharField(max_length=50, default='fa-box', verbose_name='Иконка')
    description = models.TextField(blank=True, verbose_name='Описание')
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    sku = models.CharField(max_length=50, verbose_name='Артикул', blank=True, null=True, unique=True)
    barcode = models.CharField(max_length=13, verbose_name='Штрих-код', blank=True, null=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name='Категория')
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    quantity = models.IntegerField(default=0, verbose_name='Количество на складе')
    unit = models.CharField(max_length=20, default='кг', verbose_name='Единица измерения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_low_stock(self):
        return self.quantity < 10
    

class ProductInstance(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='instances', verbose_name='Товар')
    serial_number = models.CharField(max_length=100, unique=True, verbose_name='Индивидуальный номер')
    expiry_date = models.DateField(null=True, blank=True, verbose_name='Срок годности')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата поступления')
    is_sold = models.BooleanField(default=False, verbose_name='Продан')

    class Meta:
        verbose_name = 'Экземпляр товара'
        verbose_name_plural = 'Экземпляры товаров'

    def __str__(self):
        return f"{self.product.name} SN:{self.serial_number} (Годен до: {self.expiry_date})"

    @property
    def is_expired(self):
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False

class PriceHistory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_history', verbose_name='Товар')
    old_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Старая цена')
    new_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Новая цена')
    changed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата изменения')
    changed_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, verbose_name='Изменил')
    
    class Meta:
        verbose_name = 'История цен'
        verbose_name_plural = 'История цен'
        ordering = ['-changed_at']
    
    def __str__(self):
        return f"{self.product.name}: {self.old_price} -> {self.new_price}"

class Supply(models.Model):
    supplier = models.CharField(max_length=200, verbose_name='Поставщик')
    supply_date = models.DateTimeField(default=timezone.now, verbose_name='Дата поставки')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая стоимость')
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, verbose_name='Создал')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    
    class Meta:
        verbose_name = 'Поставка'
        verbose_name_plural = 'Поставки'
        ordering = ['-supply_date']
    
    def __str__(self):
        return f"Поставка №{self.id} от {self.supplier} ({self.supply_date.strftime('%d.%m.%Y')})"
    
    def calculate_total(self):
        """Пересчитать общую стоимость поставки"""
        total = sum(item.get_total() for item in self.items.all())
        self.total_cost = total
        self.save()
        return total

class SupplyItem(models.Model):
    """Позиция в поставке (один товар)"""
    supply = models.ForeignKey(Supply, on_delete=models.CASCADE, related_name='items', verbose_name='Поставка')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='supply_items', verbose_name='Товар')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    
    class Meta:
        verbose_name = 'Позиция поставки'
        verbose_name_plural = 'Позиции поставки'
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.product.unit}"
    
    def get_total(self):
        """Получить сумму по позиции"""
        return self.quantity * self.price_per_unit
    
    def save(self, *args, **kwargs):
        # Если цена не указана, берем текущую цену товара
        if not self.price_per_unit:
            self.price_per_unit = self.product.price
        is_new = self.pk is None
        super().save(*args, **kwargs)
        # Увеличиваем количество товара на складе только при создании
        if is_new:
            self.product.quantity += float(self.quantity)
            self.product.save()
        # Пересчитываем общую стоимость поставки
        self.supply.calculate_total()
