# Generated by Django 4.1.13 on 2024-08-29 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venture', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='venture',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
