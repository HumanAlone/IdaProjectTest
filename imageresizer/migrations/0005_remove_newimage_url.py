# Generated by Django 3.1.7 on 2021-02-23 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imageresizer', '0004_auto_20210222_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newimage',
            name='url',
        ),
    ]
