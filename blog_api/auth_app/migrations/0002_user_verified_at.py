# Generated by Django 4.2.9 on 2024-01-29 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auth_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="verified_at",
            field=models.DateTimeField(null=True),
        ),
    ]
