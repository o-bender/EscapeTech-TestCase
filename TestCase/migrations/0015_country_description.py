# Generated by Django 2.1.3 on 2018-11-12 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestCase', '0014_auto_20181112_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='description',
            field=models.TextField(null=True),
        ),
    ]