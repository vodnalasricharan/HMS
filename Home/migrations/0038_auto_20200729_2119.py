# Generated by Django 3.0.8 on 2020-07-29 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0037_auto_20200729_1528'),
    ]

    operations = [
        migrations.AddField(
            model_name='appeal',
            name='actual_in',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='appeal',
            name='actual_out',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
