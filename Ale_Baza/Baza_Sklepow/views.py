from django.shortcuts import render, HttpResponse

# Create your views here.
def showListaSklepow(request):
    return HttpResponse('ListaProduktow')