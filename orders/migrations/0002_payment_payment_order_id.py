# Generated by Django 4.0.8 on 2022-11-14 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
