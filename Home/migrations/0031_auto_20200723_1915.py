# Generated by Django 3.0.8 on 2020-07-23 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0030_auto_20200723_1818'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appeal',
            name='in_datetime',
            field=models.DateTimeField(verbose_name='In Date&Time(yyyy/mm/dd 24hr:60min)'),
        ),
        migrations.AlterField(
            model_name='appeal',
            name='out_datetime',
            field=models.DateTimeField(verbose_name='Out Date&Time (yyyy/mm/dd 24hr:60min)'),
        ),
    ]
