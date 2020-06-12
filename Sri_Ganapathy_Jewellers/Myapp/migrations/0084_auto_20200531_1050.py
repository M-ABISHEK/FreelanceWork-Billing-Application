# Generated by Django 3.0.5 on 2020-05-31 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0083_auto_20200528_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chitbill',
            name='End_Date',
            field=models.DateField(default='2020-05-31'),
        ),
        migrations.AlterField(
            model_name='chitbill',
            name='Start_Date',
            field=models.DateField(default='2020-05-31'),
        ),
        migrations.AlterField(
            model_name='repair',
            name='Given_Date',
            field=models.CharField(default='2020-05-31', max_length=16),
        ),
        migrations.AlterField(
            model_name='stockadd',
            name='Date',
            field=models.DateField(default='2020-05-31'),
        ),
        migrations.CreateModel(
            name='Oldjewel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight_in_grams', models.CharField(default='', max_length=16)),
                ('Nature', models.CharField(choices=[('916', '916'), ('Ordinary', 'Ordinary')], default='916', max_length=16)),
                ('Amount', models.CharField(default='', max_length=16)),
                ('Bill', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Myapp.BillingItems')),
            ],
        ),
    ]
