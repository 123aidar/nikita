from django.db import models
from django.utils import timezone
from products.models import Product

class WriteOff(models.Model):
    REASON_CHOICES = (
        ('expired', 'Истёк срок годности'),
        ('damaged', 'Повреждено'),
        ('quality', 'Несоответствие качеству'),
        ('other', 'Другое'),
    )
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='write_offs', verbose_name='Товар')
    quantity = models.IntegerField(verbose_name='Количество')
    reason = models.CharField(max_length=20, choices=REASON_CHOICES, verbose_name='Причина списания')
    reason_detail = models.TextField(blank=True, verbose_name='Детали')
    write_off_date = models.DateTimeField(default=timezone.now, verbose_name='Дата списания')
    created_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, verbose_name='Создал')
    
    class Meta:
        verbose_name = 'Списание'
        verbose_name_plural = 'Списания'
        ordering = ['-write_off_date']
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} {self.product.unit} ({self.get_reason_display()})"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Обновляем количество товара на складе
        self.product.quantity -= self.quantity
        self.product.save()

class Inventory(models.Model):
    session_id = models.CharField(max_length=50, verbose_name='ID сессии', db_index=True, default='default_session')  # Для группировки
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories', verbose_name='Товар')
    expected_quantity = models.IntegerField(verbose_name='Ожидаемое количество')
    actual_quantity = models.IntegerField(verbose_name='Фактическое количество')
    difference = models.IntegerField(verbose_name='Разница')
    inventory_date = models.DateTimeField(default=timezone.now, verbose_name='Дата инвентаризации')
    conducted_by = models.ForeignKey('accounts.CustomUser', on_delete=models.SET_NULL, null=True, verbose_name='Проводил')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    
    class Meta:
        verbose_name = 'Инвентаризация'
        verbose_name_plural = 'Инвентаризации'
        ordering = ['-inventory_date']
    
    def __str__(self):
        return f"{self.product.name} ({self.inventory_date.strftime('%d.%m.%Y')})"
    
    def save(self, *args, **kwargs):
        self.difference = self.actual_quantity - self.expected_quantity
        super().save(*args, **kwargs)
        # Обновляем количество товара на складе
        self.product.quantity = self.actual_quantity
        self.product.save()
