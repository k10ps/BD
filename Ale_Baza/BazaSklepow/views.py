from django.shortcuts import render, HttpResponse, redirect 
from .models import ListaSklepow
from .models import ListaProduktow
from .forms import OpinionForm
from reviews.models import ListaOpinii
from django.db import connection
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Użyj bezpośredniego renderowania bez GUI
import matplotlib.pyplot as plt
import io
import base64

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
    produkty_list = []
    for row in produkty:
        produkt_id = row[0]
        najnizsza_cena = showLowestPrice(produkt_id)  #szukanie najlepszej cent
        produkty_list.append({
            'id': produkt_id,
            'marka': row[1],
            'model': row[2],
            'cena': najnizsza_cena['cena'] if najnizsza_cena else None,
        })
    
    
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
    best_price=showLowestPrice(produkt_id)
    specyfikacja_list = showSpecyfikacja(kategoria, produkt_id)
    opinie_list=showOpinie(produkt_id)
    image_base64=showHistoriaCen(produkt_id)
    #dodawanie opinii
    if request.method == 'POST':
        opinia_text = request.POST.get('opinia')
        if opinia_text:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO listaopinii (id_produktu, opinia, data) VALUES (%s, %s, %s)",
                    [produkt_id, opinia_text, datetime.now()]
                )
            return redirect('produktPage', kategoria=kategoria, produkt_id=produkt_id)
    
    
    return render(request, 'produktPage.html', {
        'produkt': produkt_list, 
        'specyfikacja': specyfikacja_list, 
        'opinie': opinie_list, 
        'historia_cen_wykres': image_base64,
        'najlepsza_cena': best_price,
        }
        )

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
                "SELECT `przekatna_(cal)`, `odswiezanie_(Hz)`, `rozdzielczość`, `typ_wyswietlacza`, `glosniki_`, `proporcje_ekranu` FROM monitor WHERE id=%s",
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

def showHistoriaCen(produkt_id):
    #wykres historii cen
    with connection.cursor() as cursor:
        # Pobierz ID i nazwy sklepów dla danego produktu
        cursor.execute("SELECT id, nazwa FROM listaSklepow WHERE id_produktu=%s", [produkt_id])
        sklepy = cursor.fetchall()
        sklepy_dict = {sklep[0]: sklep[1] for sklep in sklepy}  # Słownik {id_sklepu: nazwa_sklepu}

        # Pobierz ceny i daty dla każdego sklepu
        historiacen = {}
        for sklep_id in sklepy_dict.keys():
            cursor.execute("SELECT cena, data FROM historiacen WHERE id_sklepu_z_danym_produktem=%s", [sklep_id])
            ceny_daty = cursor.fetchall()
            historiacen[sklep_id] = ceny_daty

    # Sprawdź, czy są dane do wykresu
    if any(historiacen.values()):
        # Generowanie wykresu
        plt.figure(figsize=(10, 6))

        for sklep_id, ceny_daty in historiacen.items():
            if ceny_daty:
                ceny = [cena for cena, data in ceny_daty]
                daty = [data for cena, data in ceny_daty]
                plt.plot(daty, ceny, marker='o', label=sklepy_dict[sklep_id])

        # Ustawienia wykresu
        plt.title('Historia Cen Produktu')
        plt.xlabel('Data')
        plt.ylabel('Cena (zł)')
        plt.legend()
        plt.grid(True)

        # Konwersja wykresu do formatu obrazu
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        buf.close()
        plt.close()
        return image_base64
    else:
        return None

def showLowestPrice(produkt_id):
    with connection.cursor() as cursor:
        # Pobierz ID i nazwy sklepów dla danego produktu
        cursor.execute("SELECT id, nazwa FROM listaSklepow WHERE id_produktu=%s", [produkt_id])
        sklepy = cursor.fetchall()
        sklepy_dict = {sklep[0]: sklep[1] for sklep in sklepy}  # Słownik {id_sklepu: nazwa_sklepu}

        # Pobierz ceny i daty dla każdego sklepu
        lowest_price = None
        lowest_price_date = None
        lowest_price_store = None

        for sklep_id, sklep_name in sklepy_dict.items():
            cursor.execute("SELECT cena, data FROM historiacen WHERE id_sklepu_z_danym_produktem=%s ORDER BY data DESC", [sklep_id])
            ceny_daty = cursor.fetchall()
            for cena, data in ceny_daty:
                if lowest_price is None or cena < lowest_price or (cena == lowest_price and data > lowest_price_date):
                    lowest_price = cena
                    lowest_price_date = data
                    lowest_price_store = sklep_name

    if lowest_price is not None:
        return {
            'cena': lowest_price,
            'data': lowest_price_date,
            'sklep': lowest_price_store,
        }
    else:
        return None

        
