# Generated by Django 3.2.12 on 2022-06-28 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learning_resources", "0013_add_file_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="learningobjectfile",
            name="file_route",
            field=models.CharField(max_length=200),
        ),
    ]