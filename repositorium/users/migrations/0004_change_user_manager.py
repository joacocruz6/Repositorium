# Generated by Django 3.2.12 on 2022-06-28 23:44

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_add_system_creator_email"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="user",
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
