# Generated by Django 3.0.8 on 2020-07-23 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0016_auto_20200723_1205'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appeal',
            name='address',
            field=models.CharField(max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='appeal',
            name='staff',
            field=models.CharField(max_length=200, null=True),
        ),
    ]