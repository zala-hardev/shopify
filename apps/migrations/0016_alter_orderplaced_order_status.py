# Generated by Django 5.0.4 on 2024-06-17 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0015_alter_orderplaced_razor_pay_order_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='order_status',
            field=models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('Out For Delivery', 'Out For Delivery'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel')], default='Pending', max_length=80),
        ),
    ]
