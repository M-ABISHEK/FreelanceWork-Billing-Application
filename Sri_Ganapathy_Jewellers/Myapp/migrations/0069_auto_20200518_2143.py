# Generated by Django 3.0.5 on 2020-05-18 16:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0068_auto_20200518_1825'),
    ]

    operations = [
        migrations.RenameField(
            model_name='billingpayment',
            old_name='Previous_Balance',
            new_name='Total',
        ),
        migrations.RemoveField(
            model_name='billingpayment',
            name='Total_Balance',
        ),
        migrations.AddField(
            model_name='billingpayment',
            name='Discount',
            field=models.CharField(default='0', max_length=8),
        ),
    ]
