# Generated by Django 4.1.13 on 2024-09-09 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]