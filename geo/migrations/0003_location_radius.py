# Generated by Django 5.1.9 on 2025-06-10 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_location_created_at_location_updated_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='radius',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
