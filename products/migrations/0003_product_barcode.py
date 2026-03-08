# Generated migration for adding barcode field

from django.db import migrations, models
import random


def generate_barcode():
    """Generate a unique EAN-13 barcode starting with 200 (internal use)"""
    # EAN-13 format: 12 digits + 1 check digit
    # Start with 200-299 for internal barcodes
    base = '200' + ''.join([str(random.randint(0, 9)) for _ in range(9)])
    
    # Calculate EAN-13 check digit
    odd_sum = sum(int(base[i]) for i in range(0, 12, 2))
    even_sum = sum(int(base[i]) for i in range(1, 12, 2))
    check_digit = (10 - ((odd_sum + even_sum * 3) % 10)) % 10
    
    return base + str(check_digit)


def populate_barcodes(apps, schema_editor):
    """Generate barcodes for existing products"""
    Product = apps.get_model('products', 'Product')
    existing_barcodes = set()
    
    for product in Product.objects.all():
        if not product.barcode:
            # Generate unique barcode
            barcode = generate_barcode()
            while barcode in existing_barcodes or Product.objects.filter(barcode=barcode).exists():
                barcode = generate_barcode()
            
            product.barcode = barcode
            product.save()
            existing_barcodes.add(barcode)


def reverse_barcodes(apps, schema_editor):
    """Clear barcodes when reversing migration"""
    Product = apps.get_model('products', 'Product')
    Product.objects.all().update(barcode=None)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_alter_supplyitem_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='barcode',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True, verbose_name='Штрих-код'),
        ),
        migrations.RunPython(populate_barcodes, reverse_barcodes),
    ]
