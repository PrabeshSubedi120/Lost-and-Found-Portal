# Generated by Django 5.2.4 on 2025-07-11 04:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('Lost', 'Lost'), ('Found', 'Found')], max_length=10)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=100)),
                ('contact_info', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='items/')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
