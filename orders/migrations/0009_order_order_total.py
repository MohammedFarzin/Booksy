# Generated by Django 4.0.8 on 2022-11-16 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_remove_orderproduct_variation_orderproduct_variation'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_total',
            field=models.FloatField(null=True),
        ),
    ]
