# Generated by Django 5.1.2 on 2024-10-26 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_services'),
    ]

    operations = [
        migrations.AddField(
            model_name='services',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='services_image/'),
        ),
    ]
