# Generated by Django 3.2.12 on 2022-05-02 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_add_systems_user_field"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="systems",
        ),
    ]
