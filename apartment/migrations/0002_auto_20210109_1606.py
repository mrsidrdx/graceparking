# Generated by Django 3.1.5 on 2021-01-09 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='generatesticker',
            name='bar_code',
        ),
        migrations.RemoveField(
            model_name='generatesticker',
            name='qr_code',
        ),
        migrations.AddField(
            model_name='generatesticker',
            name='qr_code_file',
            field=models.FileField(default='', upload_to=''),
        ),
    ]
