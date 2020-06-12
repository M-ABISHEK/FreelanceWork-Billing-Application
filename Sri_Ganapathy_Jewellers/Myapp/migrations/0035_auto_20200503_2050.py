# Generated by Django 3.0.5 on 2020-05-03 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0034_auto_20200503_1754'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockpaid',
            name='Date_Paid',
            field=models.CharField(default='', max_length=16),
        ),
        migrations.AlterField(
            model_name='stock',
            name='Item_Type',
            field=models.CharField(choices=[('Necklace', 'Necklace'), ('Bracelet', 'Bracelet'), ('nethichuti', 'nethichuti'), ('Bangles', 'Bangles'), ('Kaapu', 'Kaapu'), ('ArnaKayiru', 'ArnaKayiru'), ('Ottiyanam', 'Ottiyanam'), ('vangi', 'vangi'), ('chain', 'chain'), ('Anklets', 'Anklets'), ('Metti', 'Metti'), ('Aaram', 'Aaram'), ('Ring', 'Ring'), ('kammal', 'kammal'), ('Mookuthi', 'Mookuthi')], default='Ring', max_length=32),
        ),
    ]
