# Generated by Django 4.2.2 on 2023-06-29 10:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("daters", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="dateruser",
            name="match",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
