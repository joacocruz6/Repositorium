# Generated by Django 3.2.12 on 2022-04-07 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("learning_resources", "0006_create_category_model")]

    operations = [
        migrations.RenameField(
            model_name="learningobject", old_name="used_by", new_name="rated_by"
        ),
        migrations.RenameField(
            model_name="learningobject", old_name="name", new_name="title"
        ),
    ]
