# Generated by Django 3.0.5 on 2020-05-24 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0077_auto_20200522_0739'),
    ]

    operations = [
        migrations.AddField(
            model_name='billingpayment',
            name='Balance',
            field=models.CharField(blank=True, default='0', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='billingpayment',
            name='CGST_Tax',
            field=models.CharField(blank=True, default='0', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='billingpayment',
            name='IGST_Tax',
            field=models.CharField(blank=True, default='0', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='billingpayment',
            name='SGST_Tax',
            field=models.CharField(blank=True, default='0', max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='repair',
            name='Delivered_Date',
            field=models.CharField(default='', max_length=16),
        ),
        migrations.AlterField(
            model_name='chitbill',
            name='End_Date',
            field=models.DateField(default='2020-05-24'),
        ),
        migrations.AlterField(
            model_name='chitbill',
            name='Start_Date',
            field=models.DateField(default='2020-05-24'),
        ),
        migrations.AlterField(
            model_name='repair',
            name='Given_Date',
            field=models.CharField(default='2020-05-24', max_length=16),
        ),
        migrations.AlterField(
            model_name='stockadd',
            name='Date',
            field=models.DateField(default='2020-05-24'),
        ),
        migrations.AlterField(
            model_name='stockpaid',
            name='Date_Paid',
            field=models.DateField(default='2020-05-24'),
        ),
    ]
