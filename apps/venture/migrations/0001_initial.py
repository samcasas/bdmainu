# Generated by Django 4.1.13 on 2024-08-27 07:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('venture_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('city', models.IntegerField()),
                ('street', models.CharField(max_length=255)),
                ('external_number', models.IntegerField()),
                ('internal_number', models.IntegerField(blank=True, null=True)),
                ('cp', models.CharField(max_length=10)),
                ('suburb', models.CharField(max_length=100)),
                ('country', models.IntegerField()),
                ('state', models.IntegerField()),
                ('phone', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Venture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('keywords', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
