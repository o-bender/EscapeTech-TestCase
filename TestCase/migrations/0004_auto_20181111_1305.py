# Generated by Django 2.1.3 on 2018-11-11 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TestCase', '0003_users_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(default=None, max_length=254, unique=True),
        ),
    ]