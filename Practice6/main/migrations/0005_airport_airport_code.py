# Generated by Django 5.0.1 on 2024-03-02 11:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0004_aircraft_full_name"),
    ]

    operations = [
        migrations.AddField(
            model_name="airport",
            name="airport_code",
            field=models.CharField(
                default=1,
                max_length=3,
                validators=[django.core.validators.MinLengthValidator(3)],
            ),
            preserve_default=False,
        ),
    ]
