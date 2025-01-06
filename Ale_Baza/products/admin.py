from django.contrib import admin, messages
from django.db import connection, transaction
from django.core.exceptions import ValidationError
from .models import ListaProduktow, Telewizor, Komputer, Monitor, Procesor, Ram
from .inline import TelewizorInline, MonitorInline, KomputerInline, ProcesorInline, RamInline


#dodawanie do listaProduktow
class ListaProduktowAdmin(admin.ModelAdmin):
    list_display=['id', 'kategoria', 'marka', 'model']
    list_filter = ['kategoria', 'marka']
    search_fields = ['kategoria', 'marka', 'model']
    
    actions=['usun_produkt']
    
    #wylaczenie wbudowanego usuwania obiektu w django
    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = [
        ("Podstawowe informacje o produkcie", {'fields': ['kategoria', 'marka', 'model'],}),
    ]
    inlines = [TelewizorInline, MonitorInline, KomputerInline, ProcesorInline, RamInline]

    #usuwanie produktu
    def usun_produkt(self, request, queryset):
        produkt_ids = [produkty.id for produkty in queryset]
        
        if not produkt_ids:
            messages.error(request, "Nie wybrano żadnych obiektów do usunięcia.", level=messages.WARNING)
            return

        with transaction.atomic():
            with connection.cursor() as cursor:
                #1. usun powiazane opinie
                cursor.execute(
                    f"DELETE FROM listaopinii WHERE id_produktu IN %s", [tuple(produkt_ids)]
                )
                #messages.success(request, f"Usunięto opinie powiązane z {len(produkt_ids)}.")
                
                #przeszukujemy liste skelpow w poszukwianiu id
                cursor.execute(
                    f"SELECT id FROM listaSklepow WHERE id_produktu IN %s", [tuple(produkt_ids)]
                )
                sklepy_ids = [row[0] for row in cursor.fetchall()]  #zapisujemy te id i rozpakowujemy
                if sklepy_ids:
                    #2. usun z historii cen
                    cursor.execute(
                        f"DELETE FROM historiacen WHERE id_sklepu_z_danym_produktem IN %s",  [tuple(sklepy_ids)]
                    )
                    #messages.success(request, f"Usunięto historie cen powiązane z {len(produkt_ids)}.")
                #3. usun z listy sklepow
                cursor.execute(
                    f"DELETE FROM listaSklepow WHERE id IN %s", [tuple(produkt_ids)]
                )
                #messages.success(request, f"Usunięto {len(produkt_ids)} rekord(y) z listy sklepów.")
                
                #4. usun z kategorii
                cursor.execute(
                    f"SELECT DISTINCT kategoria FROM listaProduktow WHERE id IN %s", [tuple(produkt_ids)]
                )
                kategorie=cursor.fetchall()
                for (each_kat,) in kategorie: #przelatujemy przez kazda kategorie
                    #usuwamy kazdy rekord pwoaizany
                    #dla ram i procesor
                    if each_kat=='RAM' or each_kat=='Ram' or each_kat=='ram':
                        cursor.execute(f"SELECT id FROM komputer WHERE pamiec_ram IN %s", [tuple(produkt_ids)])
                        kom_id=[row[0] for row in cursor.fetchall()]
                        if kom_id:
                            messages.info(request, f"Istnieje komputer {len(kom_id)} z tym podzespołem. NIE MOŻNA USUNĄĆ")
                            return
                        cursor.execute(f"DELETE FROM {each_kat} WHERE id IN %s", [tuple(produkt_ids)])
                    elif each_kat=='PROCESOR' or each_kat=='Procesor' or each_kat=='procesor':
                        cursor.execute(f"SELECT id FROM komputer WHERE procesor IN %s", [tuple(produkt_ids)])
                        kom_id=[row[0] for row in cursor.fetchall()]
                        if kom_id:
                            messages.info(request, f"Istnieje komputer {len(kom_id)} z tym podzespołem. NIE MOŻNA USUNĄĆ")
                            return
                        cursor.execute(f"DELETE FROM {each_kat} WHERE id IN %s", [tuple(produkt_ids)])
                    
                    else: #monitor, telewizor, komputer
                        cursor.execute(f"DELETE FROM {each_kat} WHERE id IN %s", [tuple(produkt_ids)])
                
                #5. usun produkt
                cursor.execute(
                        f"DELETE FROM listaproduktow WHERE id IN %s", [tuple(produkt_ids)]
                    )
                messages.success(request, f"Usunięto {len(produkt_ids)} rekord(y) z listy sklepów.")
    usun_produkt.short_description = "Usun produkt"
    
            


    

admin.site.register(ListaProduktow, ListaProduktowAdmin)

