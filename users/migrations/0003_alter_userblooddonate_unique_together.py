# Generated by Django 4.2.5 on 2023-11-18 20:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_userblooddonate_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='userblooddonate',
            unique_together=set(),
        ),
    ]
