# Generated by Django 3.0.5 on 2020-05-25 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0080_stockpaid_totalbalance'),
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceCheck_ToBePaid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Date', models.CharField(default='[]', max_length=1024)),
                ('Amount', models.CharField(default='[]', max_length=1024)),
                ('BillItem', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Myapp.BillingItems')),
            ],
        ),
    ]
