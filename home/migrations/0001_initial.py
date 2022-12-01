# Generated by Django 4.0.8 on 2022-11-28 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('banner_picture', models.ImageField(blank=True, upload_to='photos/banner')),
                ('alt_text', models.CharField(max_length=100)),
            ],
        ),
    ]
