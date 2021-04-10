from django.urls import  path
from . import views

app_name='publis'
urlpatterns = [
	path('', views.collections, name='collections'),
	path('stats_generales/', views.stats_generales, name='stats_generales'),
	path('stats_collection/<str:code_collection>/', views.stats_collection, name='stats_collection'),
	path('classement/<str:code_collection>/', views.classement, name='classement'),
	path('referentiel/', views.referentiel, name='referentiel'),
	path('recherche/', views.recherche, name='recherche'),
	path('instructions/', views.instructions, name='instructions'),
	path('publications/', views.publications, name='publications'),
	path('publications/sql/', views.sql, name='sql'),
]
