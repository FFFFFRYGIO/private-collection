# Generated by Django 4.1.4 on 2023-01-07 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0006_alter_book_isbn_book_unique book assigment for user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="ISBN",
            field=models.IntegerField(),
        ),
    ]
