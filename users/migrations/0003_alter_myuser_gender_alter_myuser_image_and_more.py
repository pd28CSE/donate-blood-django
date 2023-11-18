# Generated by Django 4.2.5 on 2023-11-18 19:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_bloodrecipients_userblooddonate_blood_recipients_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], max_length=7),
        ),
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile-pictures'),
        ),
        migrations.CreateModel(
            name='UserDeviceToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_token', models.UUIDField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='device', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BloodNeeded',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blood_group', models.CharField(choices=[('A+', 'A RhD Positive'), ('A-', 'A RhD Negative'), ('B+', 'B RhD Positive'), ('B-', 'B RhD Negative'), ('O+', 'O RhD Positive'), ('O-', 'O RhD Negative'), ('AB+', 'AB RhD Positive'), ('AB-', 'AB RhD Negative')], max_length=5)),
                ('place', models.CharField(max_length=255)),
                ('coordinates', models.JSONField(blank=True, null=True)),
                ('date_time', models.DateTimeField()),
                ('hospital_name', models.CharField(blank=True, max_length=255, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('blood_recipients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blood_needs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
