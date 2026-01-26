from django import forms
from .models import WriteOff, Inventory
from products.models import Product

class WriteOffForm(forms.ModelForm):
    class Meta:
        model = WriteOff
        fields = ['product', 'quantity', 'reason', 'reason_detail']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'reason': forms.Select(attrs={'class': 'form-control'}),
            'reason_detail': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем data-атрибут category к каждому товару для фильтрации
        product_field = self.fields['product']
        product_choices = []
        for product in Product.objects.all():
            product_choices.append((product.id, product.name))
        product_field.choices = [('', '---------')] + product_choices
        # Добавляем data-атрибуты через JavaScript или модифицируем widget
        self.fields['product'].widget.attrs['class'] = 'form-select'

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ['product', 'expected_quantity', 'actual_quantity', 'notes']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'expected_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'actual_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Добавляем data-атрибут category к каждому товару для фильтрации
        self.fields['product'].widget.attrs['class'] = 'form-select'
        if 'instance' not in kwargs:
            # При создании новой инвентаризации автоматически заполняем ожидаемое количество
            self.fields['expected_quantity'].widget.attrs['readonly'] = False
