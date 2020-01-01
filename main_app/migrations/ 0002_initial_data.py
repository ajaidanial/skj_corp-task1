"""This file loads the initial data into the database on `migrate`."""
from django.db import migrations

from main_app.models import BaseUser
from task1.settings import ADMIN_USER


def create_super_user(apps, schema_editor):
    # create the app super user
    BaseUser.objects.create_superuser(
        email=ADMIN_USER["email"], password=ADMIN_USER["password"],
    )


def delete_super_user(apps, schema_editor):
    # delete the app super user
    BaseUser.objects.get(email=ADMIN_USER["email"]).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("main_app", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_super_user, reverse_code=delete_super_user),
    ]
