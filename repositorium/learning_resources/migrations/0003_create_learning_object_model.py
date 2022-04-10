# Generated by Django 3.2.12 on 2022-03-13 21:31

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("learning_resources", "0002_create_system_model"),
    ]

    operations = [
        migrations.CreateModel(
            name="LearningObject",
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
                ("content", models.TextField()),
                (
                    "categories",
                    models.ManyToManyField(
                        related_name="learning_objects",
                        to="learning_resources.Categories",
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "forked",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="learning_resources.learningobject",
                    ),
                ),
            ],
            options={"abstract": False},
        )
    ]