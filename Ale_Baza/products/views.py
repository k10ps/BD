from django.shortcuts import render, HttpResponse
from models import *
from django.db import connection

# Create your views here.
def showListaSklepow(request):
    with connection.cursor() as c:
        c.execute("SELECT * FROM ListaProduktow")
        #tłumaczenie na liste krotek
        rows = c.fetchall()

        for row in rows:
            print(f"Row: {row}")

    return HttpResponse("Zapytanie SQL showListaSklepow wykonane, sprawdź konsolę.")