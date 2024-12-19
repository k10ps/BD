from django.shortcuts import render, HttpResponse
from BazaSklepow.models import ListaProduktow
from django.db import connection

# Create your views here.
def showListaProduktow(request):
    with connection.cursor() as c:
        c.execute("SELECT * FROM ListaProduktow")
        #tłumaczenie na liste krotek
        rows = c.fetchall()

        for row in rows:
            print(f"Row: {row}")

    return HttpResponse("Zapytanie SQL showListaProduktow wykonane, sprawdź konsolę.")

def showKategoria(request, kategoria):
    with connection.cursor() as c:
        c.execute("SELECT * FROM ListaProduktow WHERE kategoria = %s", [kategoria])
        #tłumaczenie na liste krotek
        rows = c.fetchall()
        
        if not rows:
            # Jeżeli brak wyników, wyświetlamy komunikat
            return HttpResponse(f"Brak produktów w kategorii '{kategoria}'.")
        else:
            # Jeżeli są wyniki, wyświetlamy je w konsoli
            for row in rows:
                print(f"Row: {row}")

    return HttpResponse("Zapytanie SQL showKategoria wykonane, sprawdź konsolę.")