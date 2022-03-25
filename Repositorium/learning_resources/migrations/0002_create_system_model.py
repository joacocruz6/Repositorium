# Generated by Django 3.2.12 on 2022-03-11 00:38

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("learning_resources", "0001_create_categories_model")]

    operations = [
        migrations.CreateModel(
            name="System",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=150)),
            ],
            options={"abstract": False},
        )
    ]
