# Generated by Django 3.1.7 on 2021-02-23 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageresizer', '0007_remove_newimage_resized_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='newimage',
            name='is_copy',
            field=models.BooleanField(default=False),
        ),
    ]
