# -*- coding: utf-8 -*-
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Product
from accounts.models import CustomUser


@receiver(pre_save, sender=Product)
def check_product_stock(sender, instance, **kwargs):
    """Отправляет email заведующему, когда товар достигает нулевого остатка"""
    if instance.pk:  # Только для существующих товаров
        try:
            old_product = Product.objects.get(pk=instance.pk)
            # Если количество стало 0 (было больше, стало 0)
            if old_product.quantity > 0 and instance.quantity == 0:
                # Получаем email заведующего
                managers = CustomUser.objects.filter(role='manager')
                recipients = list(managers.values_list('email', flat=True))
                
                # Фильтруем пустые email
                recipients = [email for email in recipients if email]
                
                if recipients:
                    subject = f'⚠️ Товар "{instance.name}" закончился на складе'
                    message = f'''
Уважаемый заведующий!

Товар "{instance.name}" достиг нулевого остатка на складе.

Категория: {instance.category.name}
Цена: {instance.price} руб.
Единица измерения: {instance.unit}

Необходимо оформить поставку данного товара.

---
Система управления продуктовым магазином "На Просторной"
'''
                    
                    try:
                        send_mail(
                            subject,
                            message,
                            settings.DEFAULT_FROM_EMAIL,
                            recipients,
                            fail_silently=False,
                        )
                    except Exception as e:
                        print(f"Ошибка отправки email: {e}")
        except Product.DoesNotExist:
            pass
