from django.urls import path, include
from TestCase import views


urlpatterns = [
    path('', views.index, name='index'),
    path('users', views.users, name='list_users'),
    path('foto', views.foto_album, name=views.foto_album.__name__),
]