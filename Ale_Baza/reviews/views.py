from django.shortcuts import render, HttpResponse
from django.db import connection

# Create your views here.
def showOpinie(produkt, cursor):

    query_opi = f"SELECT * FROM listaopinii WHERE id_produktu = %s"

    cursor.execute(query_opi, [produkt])  # Zabezpieczamy zapytanie wstawiając id produktu
    rows_opi = cursor.fetchall()

    if not rows_opi:
        return HttpResponse(f"Brak opinii o produkcie o id {produkt}")
    else:
        for opinia in rows_opi:
            print(f"Opinia {opinia.index}: {opinia}")  # Wypisz specyfikacje produktu
    return()