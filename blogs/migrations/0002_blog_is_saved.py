# Generated by Django 5.0 on 2024-05-01 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='is_saved',
            field=models.BooleanField(default=False),
        ),
    ]
