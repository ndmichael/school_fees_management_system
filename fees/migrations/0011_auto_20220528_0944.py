# Generated by Django 3.1.6 on 2022-05-28 08:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0010_auto_20220528_0943'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='remark',
            name='user',
        ),
        migrations.AddField(
            model_name='remark',
            name='student',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='remark', to='fees.student'),
        ),
    ]
