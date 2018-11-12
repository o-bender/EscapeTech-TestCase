from django.db import models
import uuid


class Country(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.TextField(unique=True)
    description = models.TextField(null=True)


class Eyes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    eyes_color = models.TextField(unique=True)
    description = models.TextField(null=True)


class Users(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    firstname = models.TextField()
    surname = models.TextField()
    fathername = models.TextField()
    birthdate = models.DateField()
    email = models.EmailField(null=False, default=None, unique=True)
    password = models.CharField(max_length=64, null=False, default=None)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, to_field='country', default='Russia')
    eyes_color = models.ForeignKey(Eyes, on_delete=models.CASCADE, to_field='eyes_color', default='Blue')


class FotoAlbum(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.TextField(unique=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True)


class Foto(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    album = models.ForeignKey(FotoAlbum, on_delete=models.CASCADE, to_field='title', default='default')
    description = models.TextField(null=True)
    foto = models.ImageField(upload_to='static/foto')
    middle = models.ImageField(upload_to='static/foto/middle', null=True)
    thumbnail = models.ImageField(upload_to='static/foto/thumbnail', null=True)
    user = models.ForeignKey('Users', on_delete=models.CASCADE, null=True)
