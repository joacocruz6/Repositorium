# Generated by Django 3.2.12 on 2022-04-19 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learning_resources", "0007_change_learning_object_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="learningobject",
            name="created_by",
        ),
        migrations.AddField(
            model_name="learningobject",
            name="creator_email",
            field=models.EmailField(
                db_index=True, default="jeremy@barbay.com", max_length=254
            ),
            preserve_default=False,
        ),
    ]
