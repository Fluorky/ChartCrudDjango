# Generated by Django 4.2.1 on 2023-06-13 08:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chartapp", "0009_logs_product_id_alter_logs_date_of_event_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="logs",
            name="date_of_event",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime(2023, 6, 13, 10, 16, 4, 864570)
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="date_of_last_one",
            field=models.DateTimeField(
                blank=True, default=datetime.datetime(2023, 6, 13, 10, 16, 4, 863571)
            ),
        ),
    ]