# Generated by Django 3.0.5 on 2020-04-15 02:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ShopCustomers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Customer_id', models.IntegerField()),
                ('FirstName', models.CharField(max_length=64)),
                ('LastName', models.CharField(max_length=64)),
                ('DOB', models.DateField()),
                ('PhoneNumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ShopHandlersSignUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ShopHandlers_id', models.IntegerField(default='')),
                ('NickName', models.CharField(default='None', max_length=64)),
                ('Sex', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=32)),
                ('DOB', models.DateField()),
                ('PhoneNumber', models.IntegerField()),
                ('Alt_PhoneNumber', models.IntegerField()),
                ('Shop_Name', models.CharField(default='Sri Ganapathy Jewellers', max_length=64)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
