# Generated by Django 4.1.4 on 2023-01-07 06:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0009_alter_book_authors"),
    ]

    operations = [
        migrations.AlterField(
            model_name="book",
            name="ISBN",
            field=models.CharField(max_length=13),
        ),
    ]
