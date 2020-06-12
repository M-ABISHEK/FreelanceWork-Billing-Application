# Generated by Django 3.0.5 on 2020-05-10 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0052_auto_20200510_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repair',
            name='Item_Type',
            field=models.CharField(choices=[('Bracelet', 'Bracelet'), ('Kaapu', 'Kaapu'), ('Necklace', 'Necklace'), ('Metti', 'Metti'), ('vangi', 'vangi'), ('Anklets', 'Anklets'), ('Ring', 'Ring'), ('ArnaKayiru', 'ArnaKayiru'), ('kammal', 'kammal'), ('Bangles', 'Bangles'), ('Mookuthi', 'Mookuthi'), ('nethichuti', 'nethichuti'), ('Ottiyanam', 'Ottiyanam'), ('chain', 'chain'), ('Aaram', 'Aaram')], default='[]', max_length=256),
        ),
        migrations.AlterField(
            model_name='repair',
            name='Metal_Type',
            field=models.CharField(choices=[('Gold', 'Gold'), ('Silver', 'Silver'), ('Diamond', 'Diamond'), ('Platinum', 'Platinum')], default='[]', max_length=256),
        ),
        migrations.AlterField(
            model_name='stock',
            name='Item_Type',
            field=models.CharField(choices=[('Bracelet', 'Bracelet'), ('Kaapu', 'Kaapu'), ('Necklace', 'Necklace'), ('Metti', 'Metti'), ('vangi', 'vangi'), ('Anklets', 'Anklets'), ('Ring', 'Ring'), ('ArnaKayiru', 'ArnaKayiru'), ('kammal', 'kammal'), ('Bangles', 'Bangles'), ('Mookuthi', 'Mookuthi'), ('nethichuti', 'nethichuti'), ('Ottiyanam', 'Ottiyanam'), ('chain', 'chain'), ('Aaram', 'Aaram')], default='Ring', max_length=32),
        ),
    ]
