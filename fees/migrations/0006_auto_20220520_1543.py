# Generated by Django 3.1.6 on 2022-05-20 14:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fees', '0005_auto_20220520_1540'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StaffProfile',
            new_name='Staff',
        ),
        migrations.RenameModel(
            old_name='StudentProfile',
            new_name='Student',
        ),
    ]
