# Generated by Django 5.2 on 2025-04-10 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('achievements', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='achievement',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='achievements/'),
        ),
    ]
