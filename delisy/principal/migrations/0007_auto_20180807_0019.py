# Generated by Django 2.0.7 on 2018-08-06 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('principal', '0006_url_request_payload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='url',
            name='request_payload',
            field=models.CharField(max_length=1000),
        ),
    ]