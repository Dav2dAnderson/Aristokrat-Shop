# Generated by Django 5.1.2 on 2024-11-05 01:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_contact'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contact',
            old_name='summmary',
            new_name='summary',
        ),
    ]