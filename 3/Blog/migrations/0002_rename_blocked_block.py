# Generated by Django 4.2.1 on 2023-05-16 21:07

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("Blog", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Blocked",
            new_name="Block",
        ),
    ]
