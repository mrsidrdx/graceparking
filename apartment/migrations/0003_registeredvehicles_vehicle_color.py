# Generated by Django 3.1.5 on 2021-01-10 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0002_auto_20210109_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='registeredvehicles',
            name='vehicle_color',
            field=models.CharField(default='', max_length=200),
        ),
    ]
