# Generated by Django 3.2.6 on 2021-09-07 12:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_recipe'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recipe',
            old_name='time_minuts',
            new_name='time_minutes',
        ),
    ]