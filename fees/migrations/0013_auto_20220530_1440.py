# Generated by Django 3.1.6 on 2022-05-30 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0012_remark_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='remark',
            name='slug',
            field=models.SlugField(default='remark', max_length=100, unique=True),
        ),
    ]
