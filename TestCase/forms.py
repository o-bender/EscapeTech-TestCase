from django import forms
from .models import Foto


class FotoForm(forms.ModelForm):
    class Meta:
        model = Foto
        fields = ['album', 'foto', 'description']


class AlbumFotoForm(forms.Form):
    album = forms.TextInput()


class DeleteFotoForm(forms.Form):
    album = forms.TextInput()
    foto = forms.FilePathField(path='static/foto')
