from django.shortcuts import render, HttpResponse
from .models import ListaProduktow
from django.db import connection
from reviews import views as rev
from price_history import views as hist
from django import forms

# Create your views here.
# base oznacza glowna funkcje wywolujaca fukncje pod nia

#base
def showListaProduktow(request):
    with connection.cursor() as c:
        c.execute("SELECT * FROM ListaProduktow")
        #tłumaczenie na liste krotek
        rows = c.fetchall()

        for row in rows:
            print(f"Row: {row}")

    return HttpResponse("Zapytanie SQL showListaProduktow wykonane, sprawdź konsolę.")

#base
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

#base
def showProdukt(request, kategoria, produkt):
    # Ustal dozwolone kategorie produktów, np. telewizory, komputery
    dozwolone_kategorie = ['telewizor', 'komputer', 'monitor', "procesor", "ram"]
    
    # na male znaki
    kategoria = kategoria.lower()

    # Sprawdź, czy kategoria jest poprawna
    if kategoria not in dozwolone_kategorie:
        return HttpResponse("Nieprawidłowa kategoria produktu.")

    # Wykonaj zapytanie, aby znaleźć produkt o danym id
    with connection.cursor() as c:

        # zapytanie o podstawy produktu
        showPodstawaProduktu(produkt, c)

        # Dynamiczne zapytanie dla specyfikacji produktu
        showSpecyfikacje(produkt, kategoria, c)
       
        # zapytanie o opinie
        rev.showOpinie(produkt, c)

        # zapytanie o najnizsza cene
        min_cena = hist.showLowestPrice(produkt, c)
        print("Najnizsza cena: ", min_cena)
 
    return HttpResponse("Zapytanie SQL showProdukt wykonane, sprawdź konsolę.")

def showPodstawaProduktu(produkt, cursor):
    cursor.execute("SELECT * FROM ListaProduktow WHERE id = %s", [produkt])
    rows_prod = cursor.fetchall()

    if not rows_prod:
        # Jeśli brak produktu o takim id
        return HttpResponse(f"Brak produktu o id '{produkt}'.")
    else:
        print(f"Produkt: {rows_prod}")  # Wypisz produkt
    return()

def showSpecyfikacje(produkt, kategoria, cursor):
    query_spec = f"SELECT * FROM {kategoria} WHERE id = %s"

    cursor.execute(query_spec, [produkt])  # Zabezpieczamy zapytanie wstawiając id produktu
    rows_spec = cursor.fetchall()
    
    if not rows_spec:
        return HttpResponse(f"Brak specyfikacji produktu o id '{produkt}' w kategorii {kategoria}.")
    else:
        print(f"Specyfikacje: {rows_spec}")  # Wypisz specyfikacje produktu
    return()