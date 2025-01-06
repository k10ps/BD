from django.urls import path
from . import views

#path('', views.showListaSklepow)

urlpatterns = [
    path('', views.homePage, name='homePage'),  #stronaglowna
    path('produkty/<str:kategoria>/<int:produkt_id>/', views.showProdukt, name='produktPage'),
    path('produkt/<str:kategoria>/', views.showKategoria, name='produkty_by_kategoria'),
]