# Generated by Django 3.0.5 on 2020-05-01 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0026_auto_20200430_2059'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='Item_Choice',
            field=models.CharField(choices=[('961', '961'), ('Ordinary', 'Ordinary')], default='961', max_length=32),
        ),
        migrations.AddField(
            model_name='stock',
            name='Item_Type',
            field=models.CharField(choices=[('Necklace', 'Necklace'), ('kammal', 'kammal'), ('chain', 'chain'), ('nethichuti', 'nethichuti'), ('Ottiyanam', 'Ottiyanam'), ('Anklets', 'Anklets'), ('vangi', 'vangi'), ('ArnaKayiru', 'ArnaKayiru'), ('Ring', 'Ring'), ('Kaapu', 'Kaapu'), ('Mookuthi', 'Mookuthi'), ('Bracelet', 'Bracelet'), ('Aaram', 'Aaram'), ('Bangles', 'Bangles'), ('Metti', 'Metti')], default='Ring', max_length=32),
        ),
        migrations.AddField(
            model_name='stock',
            name='Quantity',
            field=models.CharField(default='', max_length=32),
        ),
    ]
