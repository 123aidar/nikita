from django import forms
from .models import Product, Category

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название категории'}),
            'icon': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'fa-box'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Описание категории'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'barcode', 'category', 'image', 'description', 'price', 'quantity', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'barcode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Штрих-код (13 цифр)'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Изменяем порядок полей
        if self.instance and self.instance.pk:
            field_order = ['name', 'barcode', 'category', 'image', 'description', 'price', 'quantity', 'unit']
            self.order_fields(field_order)

from .models import ProductInstance

class ProductInstanceForm(forms.ModelForm):
    class Meta:
        model = ProductInstance
        fields = ['product', 'serial_number', 'expiry_date']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class PriceUpdateForm(forms.Form):
    new_price = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        label='Новая цена',
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )
