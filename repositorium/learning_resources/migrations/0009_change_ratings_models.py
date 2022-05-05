# Generated by Django 3.2.12 on 2022-05-02 23:40

import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("learning_resources", "0008_change_created_by_for_creator_email"),
    ]

    operations = [
        migrations.CreateModel(
            name="LearningObjectUsage",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RemoveField(
            model_name="learningobject",
            name="rated_by",
        ),
        migrations.DeleteModel(
            name="Ratings",
        ),
        migrations.AddField(
            model_name="learningobjectusage",
            name="learning_object",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="learning_resources.learningobject",
            ),
        ),
        migrations.AddField(
            model_name="learningobjectusage",
            name="used_on",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="learning_objects_used",
                to="learning_resources.system",
            ),
        ),
        migrations.AddField(
            model_name="learningobjectusage",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="has_used",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="learningobject",
            name="used_by",
            field=models.ManyToManyField(
                through="learning_resources.LearningObjectUsage",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]