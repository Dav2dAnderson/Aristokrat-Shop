# Generated by Django 5.1.2 on 2024-11-05 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('summmary', models.CharField(max_length=250)),
                ('message', models.TextField()),
            ],
        ),
    ]
