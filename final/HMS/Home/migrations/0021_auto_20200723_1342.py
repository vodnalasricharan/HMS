# Generated by Django 3.0.8 on 2020-07-23 08:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0020_auto_20200723_1339'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appeal',
            name='staff',
            field=models.CharField(default='To be allocated', max_length=500, null=True),
        ),
    ]