# Generated by Django 3.2.5 on 2021-07-27 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_rename_prduct_cart_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderplaced',
            old_name='prduct',
            new_name='product',
        ),
    ]