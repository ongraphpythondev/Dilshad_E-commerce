# Generated by Django 3.2.5 on 2021-07-27 07:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_prduct_orderplaced_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='discription',
            new_name='description',
        ),
    ]
