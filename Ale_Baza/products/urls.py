from django.urls import path
from . import views

urlpatterns = [
    path('', views.showListaProduktow),
    path('<str:kategoria>/<str:produkt>/', views.showProdukt),
    path('<str:kategoria>/', views.showKategoria)
]