# Generated by Django 3.2.13 on 2022-06-14 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('georepo', '0007_auto_20220614_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='layerstyle',
            name='max_zoom',
            field=models.IntegerField(default=8),
        ),
        migrations.AddField(
            model_name='layerstyle',
            name='min_zoom',
            field=models.IntegerField(default=1),
        ),
    ]
