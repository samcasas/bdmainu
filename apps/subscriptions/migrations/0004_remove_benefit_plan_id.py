# Generated by Django 4.1.13 on 2024-09-24 05:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_subscription_code_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='benefit',
            name='plan_id',
        ),
    ]
