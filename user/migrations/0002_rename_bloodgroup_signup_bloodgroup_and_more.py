# Generated by Django 5.0.3 on 2024-04-19 17:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='signup',
            old_name='bloodgroup',
            new_name='bloodGroup',
        ),
        migrations.RenameField(
            model_name='signup',
            old_name='phone',
            new_name='gender',
        ),
        migrations.RemoveField(
            model_name='signup',
            name='sex',
        ),
    ]
