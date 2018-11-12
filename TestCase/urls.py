from django.urls import path, include
from TestCase import views


urlpatterns = [
    path('', views.index, name='index'),
    path('user', views.users, name='list_users'),
    path('user/update', views.update_user, name='add_user'),
    path('foto', views.get_fotos, name=views.get_fotos.__name__),
    path('foto/add', views.add_foto, name=views.add_foto.__name__),
    path('foto/delete', views.delete_foto, name=views.delete_foto.__name__),
    path('album', views.get_albums, name=views.get_albums.__name__),
    path('album/add', views.add_album, name=views.add_album.__name__),
    path('album/delete', views.delete_album, name=views.delete_album.__name__),
]