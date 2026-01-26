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
        fields = ['name', 'category', 'image', 'description', 'price', 'quantity', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'unit': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Артикул генерируется автоматически и не должен редактироваться
        if self.instance and self.instance.pk:
            self.fields['sku_display'] = forms.CharField(
                label='Артикул',
                initial=self.instance.sku,
                disabled=True,
                required=False,
                widget=forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
            )
            # Изменяем порядок полей
            field_order = ['name', 'sku_display', 'category', 'image', 'description', 'price', 'quantity', 'unit']
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
