# Generated by Django 3.1.4 on 2021-02-13 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='country',
            field=models.CharField(default='Italy', max_length=120),
        ),
    ]