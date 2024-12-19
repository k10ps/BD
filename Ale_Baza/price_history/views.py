from django.shortcuts import render, HttpResponse


# Create your views here.

def showLowestPrice(produkt, cursor):
    query = """
        SELECT MIN(cena)
        FROM historiacen
        WHERE id_sklepu_z_danym_produktem IN (
            SELECT id FROM listasklepow WHERE id_produktu = %s
        )
    """
    cursor.execute(query, [produkt])
    min_cena = cursor.fetchone()

    return(min_cena)