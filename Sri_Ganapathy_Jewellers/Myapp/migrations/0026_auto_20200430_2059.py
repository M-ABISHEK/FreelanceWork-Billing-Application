# Generated by Django 3.0.5 on 2020-04-30 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0025_auto_20200430_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='Item_id',
            field=models.CharField(default='', max_length=32, unique=True),
        ),
    ]
