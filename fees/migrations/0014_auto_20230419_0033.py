# Generated by Django 3.1.6 on 2023-04-18 23:33

from django.db import migrations, models
import fees.models


class Migration(migrations.Migration):

    dependencies = [
        ('fees', '0013_auto_20220530_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='academic_year',
            field=models.PositiveIntegerField(choices=[(2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022), (2023, 2023)], default=fees.models.current_year),
        ),
    ]
