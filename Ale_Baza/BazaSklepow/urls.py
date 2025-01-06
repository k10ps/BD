from django.urls import path
from . import views

#path('', views.showListaSklepow)

urlpatterns = [
    path('', views.homePage, name='homePage'),  #stronaglowna
    path('search/', views.search, name='search'), #wynika z paska wyszukiwania
    #kolejnosc ma znaczenia nie podmieniac
    #strona indywidualngo produktu
    path('produkty/<str:kategoria>/<int:produkt_id>/', views.showProdukt, name='produktPage'),  
    #strona produktow po kategorii
    path('produkt/<str:kategoria>/', views.showKategoria, name='produkty_by_kategoria'),    
]