# Generated by Django 3.1.7 on 2021-02-23 14:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imageresizer', '0006_newimage_resized_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newimage',
            name='resized_image',
        ),
    ]