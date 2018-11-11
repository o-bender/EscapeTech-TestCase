from django.shortcuts import render
from django.http import HttpResponse, HttpResponseForbidden
from TestCase.models import Users, Country, Eyes, FotoAlbum, Foto
from . import forms
from django.core.serializers import serialize
from datetime import datetime
import secrets
from hashlib import sha256
from functools import wraps


def Auth(f):
    @wraps(f)
    def _(request, *args, **kwargs):
        request_data = request.POST.dict() or request.GET.dict()
        email = request_data.get('email')
        try:
            user = Users.objects.get(email=email)
            password = sha256(request_data.get('password').encode()).hexdigest()
            if secrets.compare_digest(user.password, password):
                return f(request, *args, **kwargs)
            raise Users.DoesNotExist
        except Users.DoesNotExist:
            return HttpResponseForbidden("{'status': 'error', 'message': 'User name or password not valide'}")
    return _


def index(request):
    return HttpResponse(render(request,
                               'index.html',
                               context=dict(
                                   countries=Country.objects.all(),
                                   eyes=Eyes.objects.all(),
                                   albums=FotoAlbum.objects.all(),
                               )))


@Auth
def users(request):
    if request.method == 'POST':
        return add_user(request)
    return HttpResponse(serialize('json', Users.objects.all()))



def add_user(request):
    post_data = request.POST.dict()
    user = Users.objects.get(email=post_data.get('email'))

    for attr in ('firstname', 'surname', 'fathername', 'birthdate'):
        post_val = post_data.get(attr)
        if post_val:
            setattr(user, attr, post_val)

    new_password = post_data.get('new_password')
    if new_password:
        sha256(new_password.encode()).hexdigest()
        user.password = new_password

    try:
        user.country = Country.objects.get(country=post_data.get('country'))
    except Country.DoesNotExist as e:
        return HttpResponse('{"status":"error","message":"%s"}' % str(e))

    try:
        user.eyes_color = Eyes.objects.get(eyes_color=post_data.get('eyes_color'))
    except Eyes.DoesNotExist as e:
        return HttpResponse('{"status":"error","message":"%s"}' % str(e))

    user.save()
    return HttpResponse("{'status': 'ok'}")


@Auth
def foto_album(request):
    if request.method == 'POST':
        return update_foto_album(request)
    return HttpResponse(serialize('json', FotoAlbum.objects.all()))


def update_foto_album(request):
    form = forms.FotoForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        return HttpResponse('ok')
    return HttpResponse('err')
