# -*- coding: utf-8 -*-
from django.db import migrations, models


def update_directors_to_managers(apps, schema_editor):
    """Обновляет всех директоров на заведующих"""
    CustomUser = apps.get_model('accounts', 'CustomUser')
    CustomUser.objects.filter(role='director').update(role='manager')


def reverse_update(apps, schema_editor):
    """Откат изменений - не выполняется, так как роль director удалена"""
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(update_directors_to_managers, reverse_update),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(
                choices=[('manager', 'Заведующий'), ('cashier', 'Кассир')],
                default='cashier',
                max_length=20,
                verbose_name='Роль'
            ),
        ),
    ]
