# Generated by Django 3.0.5 on 2020-04-28 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0008_auto_20200428_0840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingitems',
            name='Item_type',
            field=models.CharField(default='[]', max_length=64),
        ),
    ]
