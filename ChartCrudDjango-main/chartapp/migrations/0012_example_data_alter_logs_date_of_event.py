# Generated by Django 4.2.1 on 2023-08-31 06:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chartapp", "0011_logs_ip_alter_logs_date_of_event_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Example_Data",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("hours", models.CharField(blank=True, max_length=100, unique=True)),
                ("quantity", models.IntegerField(default=None)),
                ("line1", models.IntegerField(default=None)),
                ("line2", models.IntegerField(default=None)),
                ("line3", models.IntegerField(default=None)),
            ],
        ),
        migrations.AlterField(
            model_name="logs",
            name="date_of_event",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime(2023, 8, 31, 8, 33, 58, 665184)
            ),
        ),
    ]
