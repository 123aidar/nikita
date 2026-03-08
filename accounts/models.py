# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('manager', 'Заведующий'),
        ('cashier', 'Кассир'),
    )
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='cashier', verbose_name='Роль')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"
    
    def can_manage_products(self):
        return self.role == 'manager'
    
    def can_manage_sales(self):
        return self.role in ['manager', 'cashier']
    
    def can_view_reports(self):
        return self.role == 'manager'
    
    def is_manager_or_director(self):
        # Метод оставлен для совместимости, теперь проверяет только manager
        return self.role == 'manager'
