from django.shortcuts import render, HttpResponse, redirect 
from .models import ListaSklepow
from .models import ListaProduktow
from .forms import OpinionForm
from reviews.models import ListaOpinii
from django.db import connection
from datetime import datetime

# Create your views here.
# def showListaSklepow(request):
#     data = ListaSklepow.objects.raw("SELECT * FROM Listasklepow")

#     return render(request, 'output.html',{'data': data})

#def showListaSklepow(request):

    #return HttpResponse('Witaj w bazie sklepow elektronicznych')


#funckja wyswietlajaca na stronei glwonej kategoeir
def homePage(request):
    #pobieranie unikalnych (dzieki DISTINCT) kategori z listy porduktow
    with connection.cursor() as cursor:
        cursor.execute("SELECT DISTINCT kategoria FROM listaProduktow")
        kategorie = [row[0] for row in cursor.fetchall()]
    return render(request, 'homePage.html', {'kategorie': kategorie})

def showKategoria(request, kategoria):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, marka, model FROM listaProduktow WHERE kategoria=%s", [kategoria])
        produkty = cursor.fetchall()  #zbieranie wynikow
    #przekształcanie w lsite slownikow
    produkty_list = [{'id': row[0], 'marka': row[1], 'model': row[2]} for row in produkty]
    return render(request, 'kategoriePage.html', {'produkty': produkty_list, 'kategoria': kategoria})

def showProdukt(request, kategoria, produkt_id):
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, kategoria, marka, model FROM listaProduktow WHERE id=%s", [produkt_id])
        produkt = cursor.fetchone()  #zbieranie wyniku
        produkt_list = {
            'id': produkt[0],
            'kategoria': produkt[1],
            'marka': produkt[2],
            'model': produkt[3],
        }
        
    #pobieranie danych specyfikacji, opinii
    specyfikacja_list = showSpecyfikacja(kategoria, produkt_id)
    opinie_list=showOpinie(produkt_id)
    
    #dodawanie opinii
    if request.method == 'POST':
        opinia_text = request.POST.get('opinia')
        if opinia_text:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO listaopinii (id_produktu, opinia, data) VALUES (%s, %s, %s)",
                    [produkt_id, opinia_text, datetime.now()]
                )
            return redirect('produktPage', kategoria=kategoria, produkt_id=produkt_id)
    
    #wykres historii cen
    with connection.cursor() as cursor:
        #w jakich sklepach jest dostepny obiket, by moc sprawdzic cene
        cursor.execute("SELECT id FROM listaSklepow WHERE id_produktu=%s", [produkt_id])
        sklepy = cursor.fetchall()  #zbieranie wyniku
        
        cursor.execute("SELECT cena, data FROM historiacen WHERE id_sklepu_z_danym_produktem=%s", [sklepy])
        historiacen = cursor.fetchall()  #zbieranie wyniku
       
    
    
    return render(request, 'produktPage.html', {'produkt': produkt_list, 'specyfikacja': specyfikacja_list, 'opinie': opinie_list})

def showSpecyfikacja(kategoria, produkt_id):
    # Pobierz specyfikację w zależności od kategorii
    with connection.cursor() as cursor:
        if kategoria.lower() == 'telewizor':
            cursor.execute(
                "SELECT `przekatna_(cal)`, `typ_wyswietlacza`, `rozdzielczosc_(xK)`, `smart_TV` FROM telewizor WHERE id=%s",
                [produkt_id]
            )
            specyfikacja = cursor.fetchone()
            if specyfikacja:
                specyfikacja_dict = {
                    'Przekątna (cal)': specyfikacja[0],
                    'Typ wyświetlacza': specyfikacja[1],
                    'Rozdzielczość (xK)': specyfikacja[2],
                    'Smart TV': specyfikacja[3],    
                }

        elif kategoria.lower() == 'monitor':
            cursor.execute(
                "SELECT `przekatna_(cal)`, `odswiezanie_(Hz)`, `rozdzielczosc`, `typ_wyswietlacza`, `glosniki_`, `proporcje_ekranu`FROM monitor WHERE id=%s",
                [produkt_id]
            )
            specyfikacja = cursor.fetchone()
            if specyfikacja:
                specyfikacja_dict = {
                    'Przekątna (cal)': specyfikacja[0],
                    'Odświeżanie (Hz)': specyfikacja[1],
                    'Rozdzielczość': specyfikacja[2],
                    'Typ wyświetlacza': specyfikacja[3],
                    'Głośniki': specyfikacja[4],
                    'Proporcje ekranu': specyfikacja[5],
                }

        elif kategoria.lower() == 'komputer':
            cursor.execute("SELECT `procesor`, `pamiec_ram`, `pojemnosc_dysku` FROM komputer WHERE id=%s", [produkt_id])
            specyfikacja = cursor.fetchone()
            
            cursor.execute("SELECT marka, model FROM listaproduktow WHERE id=%s", [specyfikacja[0]])
            procesor=cursor.fetchone()
            
            cursor.execute("SELECT marka, model FROM listaproduktow WHERE id=%s", [specyfikacja[1]])
            ram=cursor.fetchone()
            
            if specyfikacja:
                specyfikacja_dict = {
                    'Procesor': f"{procesor[0]} {procesor[1]}" ,
                    'Pamięć RAM': f"{ram[0]} {ram[1]}",
                    'Pojemność dysku': specyfikacja[0],
                }

        elif kategoria.lower() == 'procesor':
            cursor.execute(
                "SELECT `liczba_rdzeni`, `taktowanie`, `rodzaj_gniazda` FROM procesor WHERE id=%s",
                [produkt_id]
            )
            specyfikacja = cursor.fetchone()
            if specyfikacja:
                specyfikacja_dict = {
                    'Liczba rdzeni': specyfikacja[0],
                    'Taktowanie': specyfikacja[1],
                    'Rodzaj gniazda': specyfikacja[2],
                }

        elif kategoria.lower() == 'ram':
            cursor.execute(
                "SELECT `typ_pamieci`, `pojemnosc_(GB)`, `taktowanie_(MHz)` FROM ram WHERE id=%s",
                [produkt_id]
            )
            specyfikacja = cursor.fetchone()
            if specyfikacja:
                specyfikacja_dict = {
                    'Typ pamięci': specyfikacja[0],
                    'Pojemność (GB)': specyfikacja[1],
                    'Taktowanie (MHz)': specyfikacja[2],
                }

    return specyfikacja_dict

def showOpinie(produkt_id):
    #opinie
    #wyswietleistniejące opinie dla produktu
    with connection.cursor() as cursor:
        cursor.execute("SELECT opinia, data FROM listaopinii WHERE id_produktu=%s", [produkt_id])
        opinie = cursor.fetchall()
        opinie_list = [{'opinia': opinia[0], 'data': opinia[1]} for opinia in opinie]

    return opinie_list




