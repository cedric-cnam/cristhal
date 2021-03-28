from django.urls import  path
from . import views

app_name='publis'
urlpatterns = [
    path('', views.index, name='index'),
]