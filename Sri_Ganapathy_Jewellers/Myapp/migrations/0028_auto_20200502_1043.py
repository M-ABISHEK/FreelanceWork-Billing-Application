# Generated by Django 3.0.5 on 2020-05-02 05:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0027_auto_20200501_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='Metal_Type',
            field=models.CharField(choices=[('Gold', 'Gold'), ('Silver', 'Silver'), ('Diamond', 'Diamond'), ('Platinum', 'Platinum')], default='Gold', max_length=16),
        ),
        migrations.AlterField(
            model_name='stock',
            name='Item_Type',
            field=models.CharField(choices=[('ArnaKayiru', 'ArnaKayiru'), ('chain', 'chain'), ('Necklace', 'Necklace'), ('Ring', 'Ring'), ('Bangles', 'Bangles'), ('Bracelet', 'Bracelet'), ('kammal', 'kammal'), ('Aaram', 'Aaram'), ('Anklets', 'Anklets'), ('Mookuthi', 'Mookuthi'), ('Metti', 'Metti'), ('vangi', 'vangi'), ('Ottiyanam', 'Ottiyanam'), ('nethichuti', 'nethichuti'), ('Kaapu', 'Kaapu')], default='Ring', max_length=32),
        ),
    ]
