# Generated by Django 5.0.1 on 2024-05-03 19:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0002_client_user_id_alter_client_id_alter_manager_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="manager",
            name="user_id",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
