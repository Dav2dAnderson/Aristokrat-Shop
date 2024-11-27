# Generated by Django 5.1.2 on 2024-10-26 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_services_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='teammate_images/')),
                ('fullname', models.CharField(max_length=150)),
                ('job', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
    ]