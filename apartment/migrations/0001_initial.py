# Generated by Django 3.1.5 on 2021-01-09 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegisteredVehicles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner_name', models.CharField(default='', max_length=200)),
                ('owner_email', models.CharField(default='', max_length=200)),
                ('owner_phone_no', models.CharField(default='', max_length=200)),
                ('vehicle_name', models.CharField(default='', max_length=200)),
                ('vehicle_type', models.CharField(default='', max_length=200)),
                ('make', models.CharField(default='', max_length=200)),
                ('model', models.CharField(default='', max_length=200)),
                ('year', models.CharField(default='', max_length=200)),
                ('vin', models.CharField(default='', max_length=200)),
                ('license_tag_no', models.CharField(default='', max_length=200)),
                ('towed_count', models.PositiveIntegerField(default=0)),
                ('date_registered', models.DateField(auto_now_add=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registered_apartment', to='accounts.apartmentowners')),
            ],
        ),
        migrations.CreateModel(
            name='GenerateSticker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sticker_color', models.CharField(default='', max_length=200)),
                ('expiry_date', models.DateField(default='')),
                ('qr_code', models.CharField(default='', max_length=200)),
                ('bar_code', models.CharField(default='', max_length=200)),
                ('sticker_file', models.FileField(default='', upload_to='')),
                ('date_created', models.DateField(auto_now_add=True)),
                ('apartment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sticker_registered_apartment', to='accounts.apartmentowners')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registered_vehicle', to='apartment.registeredvehicles')),
            ],
        ),
    ]
