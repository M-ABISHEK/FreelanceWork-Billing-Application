# Generated by Django 3.0.5 on 2020-04-29 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0016_auto_20200429_1055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingitems',
            name='Date',
            field=models.CharField(default='', max_length=16),
        ),
    ]
