# Generated by Django 4.0.8 on 2022-11-16 09:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
        ('cart', '0002_cartitems_user_alter_cartitems_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='variations',
        ),
        migrations.AddField(
            model_name='cartitems',
            name='variations',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
    ]