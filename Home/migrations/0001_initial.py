# Generated by Django 3.0.8 on 2020-07-20 18:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('designation', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('name', models.CharField(max_length=200, null=True)),
                ('email', models.CharField(max_length=200, null=True)),
                ('branch', models.CharField(choices=[('CSE', 'CSE'), ('IT', 'IT'), ('EEE', 'EEE'), ('MECH', 'MECH'), ('ECE', 'ECE')], max_length=200, null=True)),
                ('hostel', models.CharField(choices=[('Godavari', 'Godavari Boys Hostel'), ('krishna', 'Krishna Girls Hostel'), ('sharadha', 'Sharadha Girls Hostel'), ('saraswathi', 'Saraswathi Girls Hostel')], max_length=200, null=True)),
                ('rollno', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('fathername', models.CharField(max_length=200, null=True)),
                ('fmobileno', models.CharField(max_length=200, null=True)),
                ('mobileno', models.CharField(max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('profile_pic', models.ImageField(default='default.png', null=True, upload_to='')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]