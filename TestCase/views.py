from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import signals
from django.core.serializers import serialize
from django.dispatch import receiver
from . import models
from . import forms
from . import tasks
import json
import secrets
import os
from hashlib import sha256
from functools import wraps


def json_response(status, message='', response_type=HttpResponse):
    return response_type(json.dumps({'status': status, 'message': message}))


def POST(f):
    @wraps(f)
    def _(request, *args, **kwargs):
        if request.method == 'POST':
            return f(request, *args, **kwargs)
        return json_response('error', 'Method not allowed', HttpResponseBadRequest)
    return _


def Auth(f):
    @wraps(f)
    def _(request, *args, **kwargs):
        request_data = request.POST.dict() or request.GET.dict()
        email = request_data.get('email')
        try:
            user = models.Users.objects.get(email=email)
            password = sha256(request_data.get('password').encode()).hexdigest()
            if secrets.compare_digest(user.password, password):
                return f(request, user=user, *args, **kwargs)
            raise models.Users.DoesNotExist
        except models.Users.DoesNotExist:
            return json_response('error', 'User name or password not valide', HttpResponseForbidden)
    return _


@receiver(signals.post_delete, sender=models.Foto)
def remove_foto(sender, instance, *args, **kwargs):
    if os.path.isfile(instance.foto.path):
        os.remove(instance.foto.path)


def index(request):
    return HttpResponse(render(request,
                               'index.html',
                               context=dict(
                                   countries=models.Country.objects.all(),
                                   eyes=models.Eyes.objects.all(),
                                   albums=models.FotoAlbum.objects.all(),
                                   fotos=models.Foto.objects.all(),
                               )))


@Auth
def users(request, *args, **kwargs):
    return HttpResponse(serialize('json', models.Users.objects.all()))


@POST
@Auth
def update_user(request, *args, **kwargs):
    post_data = request.POST.dict()
    user = models.Users.objects.get(email=post_data.get('email'))

    for attr in ('firstname', 'surname', 'fathername', 'birthdate'):
        post_val = post_data.get(attr)
        if post_val:
            setattr(user, attr, post_val)

    new_password = post_data.get('new_password')
    if new_password:
        user.password = sha256(new_password.encode()).hexdigest()

    try:
        user.country = models.Country.objects.get(country=post_data.get('country'))
    except models.Country.DoesNotExist as e:
        return json_response("error", str(e))

    try:
        user.eyes_color = models.Eyes.objects.get(eyes_color=post_data.get('eyes_color'))
    except models.Eyes.DoesNotExist as e:
        return json_response("error", str(e))

    user.save()
    return json_response('ok')


@Auth
def get_fotos(request, user, *args, **kwargs):
    album = forms.AlbumFotoForm(request.GET)
    if album.is_valid():
        fotos = models.Foto.objects.filter(album=album.data.get('album'), user=user)
        return HttpResponse(serialize('json', fotos))
    return json_response('error', 'not valid album name')


@POST
@Auth
def add_foto(request, user, *args, **kwargs):
    form = forms.FotoForm(request.POST, request.FILES)
    if form.is_valid():
        foto = form.save(commit=False)
        foto.user = user
        # foto.middle = thumbnail_image(request.FILES.get('foto'), 600, 600)
        # foto.thumbnail = thumbnail_image(request.FILES.get('foto'), 200, 200)
        foto.save()
        tasks.save_images.delay(foto.id)
        return json_response('ok')
    return json_response('error')


@POST
@Auth
def delete_foto(request, *args, **kwargs):
    foto = forms.DeleteFotoForm(request.POST, request.FILES)
    if foto.is_valid():
        try:
            models.Foto.objects.get(
                album=foto.data.get('album'),
                foto=foto.data.get('foto')).delete()
        except models.Foto.FotoDoesNotExist as e:
            json_response("error", str(e))
    return json_response("deleted")


@Auth
def get_albums(request, user, *args, **kwargs):
    return HttpResponse(serialize('json', models.FotoAlbum.objects.filter(user=user)))


@POST
@Auth
def add_album(request, *args, **kwargs):
    album = forms.AlbumFotoForm(request.POST, request.FILES)
    if album.is_valid():
        models.FotoAlbum(title=album.data.get('album')).save()
        return json_response('ok')
    return json_response('error', 'not valide album name')


@POST
@Auth
def delete_album(request, *args, **kwargs):
    album = forms.AlbumFotoForm(request.POST, request.FILES)
    if album.is_valid():
        try:
            models.FotoAlbum.objects.get(title=album.data.get('album')).delete()
            return HttpResponse('ok')
        except models.FotoAlbum.FotoAlbumDoesNotExist as e:
            json_response('error', str(e))
    return json_response('error', 'not valide album name')
