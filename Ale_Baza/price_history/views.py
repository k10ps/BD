from django.shortcuts import render, HttpResponse
from BazaSklepow.models import ListaSklepow
from django.db import connection

# Create your views here.

# def showListaSklepow(request):
#     data = ListaSklepow.objects.raw("SELECT * FROM Listasklepow")
#     print(data)
#     return render(request, 'output.html',{'data': data})

def showListaSklepow(request):
    with connection.cursor() as c:
        c.execute("SELECT * FROM Listasklepow")
        #tłumaczenie na liste krotek
        rows = c.fetchall()

        for row in rows:
            print(f"Row: {row}")

    return HttpResponse("Zapytanie SQL showListaSklepow wykonane, sprawdź konsolę.")