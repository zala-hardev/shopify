# Generated by Django 5.0.6 on 2024-06-12 08:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0007_alter_cart_color_alter_cart_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='color',
        ),
    ]
