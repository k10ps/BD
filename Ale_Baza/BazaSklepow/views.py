from django.shortcuts import render, HttpResponse
from .models import ListaSklepow
from .models import ListaProduktow

# Create your views here.
# def showListaSklepow(request):
#     data = ListaSklepow.objects.raw("SELECT * FROM Listasklepow")

#     return render(request, 'output.html',{'data': data})

#def showListaSklepow(request):

    #return HttpResponse('Witaj w bazie sklepow elektronicznych')


#funckja wyswietlajaca na stronei glwonej kategoeir
def homePage(request):
    #pobieranie unikalnych (dzieki distinct()) kategori z listy porduktow
    kategorie = ListaProduktow.objects.values('kategoria').distinct()

    return render(request, 'homePage.html', {'kategorie': kategorie})

def showKategoria(request, kategoria):
    #pobiera produkty z wybranje kategorii, po wybraniu jej na homePage
    produkty = ListaProduktow.objects.filter(kategoria=kategoria)

    return render(request, 'produkty.html', {'produkty': produkty, 'kategoria': kategoria})