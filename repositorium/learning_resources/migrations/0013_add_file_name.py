# Generated by Django 3.2.12 on 2022-06-22 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learning_resources", "0012_create_files_and_description_models"),
    ]

    operations = [
        migrations.AddField(
            model_name="learningobjectfile",
            name="name",
            field=models.CharField(default="default", max_length=50),
            preserve_default=False,
        ),
    ]