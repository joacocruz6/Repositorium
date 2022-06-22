# Generated by Django 3.2.12 on 2022-03-13 21:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("learning_resources", "0004_create_ratings_model")]

    operations = [
        migrations.AlterField(
            model_name="categories",
            name="name",
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name="learningobject",
            name="name",
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name="system",
            name="name",
            field=models.CharField(max_length=150, unique=True),
        ),
    ]
