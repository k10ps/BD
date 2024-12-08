from django.shortcuts import render, HttpResponse
from .models import ListaSklepow

# Create your views here.
def showListaSklepow(request):
    data = ListaSklepow.objects.raw("SELECT * FROM Listasklepow")

    return render(request, 'output.html',{'data': data})