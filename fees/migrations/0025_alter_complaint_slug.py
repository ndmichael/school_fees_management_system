# Generated by Django 4.2 on 2024-08-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0024_alter_complaint_reference_id_alter_complaint_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaint',
            name='slug',
            field=models.SlugField(max_length=100, unique=True),
        ),
    ]
