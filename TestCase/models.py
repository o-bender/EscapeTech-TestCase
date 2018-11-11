from django.db import models
from django import forms


class Country(models.Model):
    country = models.TextField(unique=True)


class Eyes(models.Model):
    eyes_color = models.TextField(unique=True)


class Users(models.Model):
    firstname = models.TextField()
    surname = models.TextField()
    fathername = models.TextField()
    birthdate = models.DateField()
    email = models.EmailField(null=False, default=None, unique=True)
    password = models.CharField(max_length=64, null=False, default=None)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, to_field='country', default='Russia')
    eyes_color = models.ForeignKey(Eyes, on_delete=models.CASCADE, to_field='eyes_color', default='Blue')


class FotoAlbum(models.Model):
    title = models.TextField(unique=True)


class Foto(models.Model):
    album = models.ForeignKey(FotoAlbum, on_delete=models.CASCADE, to_field='title', default='General')
    foto = models.ImageField(upload_to='static/foto')