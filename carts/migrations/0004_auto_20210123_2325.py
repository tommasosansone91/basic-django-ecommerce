# Generated by Django 3.1.4 on 2021-01-23 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cart'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='total',
            new_name='subtotal',
        ),
    ]
