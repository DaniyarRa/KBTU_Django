# Generated by Django 5.0.1 on 2024-03-02 10:52

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="airport",
            old_name="city_name",
            new_name="city",
        ),
    ]