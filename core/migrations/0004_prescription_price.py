# Generated by Django 5.2 on 2025-04-30 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_prescription_condition_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
