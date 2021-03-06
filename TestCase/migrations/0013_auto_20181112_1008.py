# Generated by Django 2.1.3 on 2018-11-12 10:08

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('TestCase', '0012_auto_20181112_1002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='eyes',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='foto',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='foto',
            name='middle',
            field=models.ImageField(height_field=600, null=True, upload_to='static/foto/middle'),
        ),
        migrations.AlterField(
            model_name='foto',
            name='thumbnail',
            field=models.ImageField(height_field=250, null=True, upload_to='static/foto/thumbnail'),
        ),
        migrations.AlterField(
            model_name='fotoalbum',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
