from django.urls import path
from . import views

#path('', views.showListaSklepow)

urlpatterns = [
    path('', views.homePage, name='homePage'),  #stronaglowna
    path('produkty/<str:kategoria>/', views.showKategoria, name='produkty_by_kategoria'),
]