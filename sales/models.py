from django.db import models
from django.utils import timezone
from decimal import Decimal
from products.models import Product

class Sale(models.Model):
    sale_date = models.DateTimeField(default=timezone.now, verbose_name='Дата продажи')
    cashier = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, verbose_name='Кассир')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name='Общая сумма')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    
    class Meta:
        verbose_name = 'Продажа'
        verbose_name_plural = 'Продажи'
        ordering = ['-sale_date']
    
    def __str__(self):
        return f"Продажа №{self.id} от {self.sale_date.strftime('%d.%m.%Y %H:%M')}"
    
    def calculate_total(self):
        """Пересчитать общую сумму продажи"""
        total = sum(item.get_total() for item in self.items.all())
        self.total_amount = total
        self.save()
        return total

class SaleItem(models.Model):
    """Позиция в продаже (один товар)"""
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items', verbose_name='Продажа')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена за единицу')
    
    class Meta:
        verbose_name = 'Позиция продажи'
        verbose_name_plural = 'Позиции продажи'
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.product.unit}"
    
    def get_total(self):
        """Получить сумму по позиции"""
        return self.quantity * self.price_per_unit
    
    def save(self, *args, **kwargs):
        # Если цена не указана, берем текущую цену товара с наценкой 15% и НДС 20%
        if not self.price_per_unit:
            self.price_per_unit = self.product.price * Decimal('1.38')  # 1.15 * 1.2 = 1.38 (+15% наценка +20% НДС)
        
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Уменьшаем количество товара на складе только при создании
        if is_new:
            self.product.quantity -= float(self.quantity)
            self.product.save()
        
        # Пересчитываем общую сумму продажи
        self.sale.calculate_total()
