# Generated by Django 5.0.9 on 2024-11-07 15:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('coursemanagement', '0003_class'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Class',
            new_name='Courses',
        ),
    ]
