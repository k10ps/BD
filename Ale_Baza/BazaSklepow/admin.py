from django.contrib import admin, messages  
from django.db import connection, transaction
from django.core.exceptions import ValidationError
from .models import ListaSklepow


class ListaSklepowAdmin(admin.ModelAdmin):
    list_display=['id', 'display_id_produktu', 'nazwa']
    actions=['usun_rekord', 'usun_sklep']
    
    list_filter = ['nazwa']
    search_fields = ['id_produktu__id', 'nazwa']
    
    #wylaczenie wbudowanego usuwania obiektu w django
    def has_delete_permission(self, request, obj=None):
        return False
    
    #modyfikuje wyswitlanie id_produktu, wcześniej 'ListaProduktow object(2)', teraz '2'
    def display_id_produktu(self, obj):
        return obj.id_produktu.id
    display_id_produktu.short_description = "ID Produktu"
    
    #uzywa wbudowanego add, ale dodaje za pomoca bezposredniego zapytania do bazy
    def zapisz(self, request, obj, form, change):
        try:
            with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO listasklepow (id_produktu, nazwa) VALUES (%s, %s)",
                        [obj.id_produktu.id, obj.nazwa]
                    )
            messages.success(request, f"Produkt został pomyślnie dodany do sklepu '{obj.nazwa}'.")
        except Exception as e:
            # Obsługa błędów
            messages.error(request, f"Błąd podczas dodawania.")
    
    
    #usuwanie pojedynczego obiektu
    def usun_rekord(self, request, queryset):
        messages.info(request, "Three credits remain in your account.")
        
        obiekt_ids = [obiekty.id for obiekty in queryset]
        
        if not obiekt_ids:
            self.message_user(request, "Nie wybrano rekordu do usunięcia.", level='error')
            return

        with transaction.atomic():
            with connection.cursor() as cursor:
                #usuwanie najpierw z historii cen
                cursor.execute(
                    "DELETE FROM historiacen WHERE id_sklepu_z_danym_produktem IN %s", 
                    [tuple(obiekt_ids)]
                )
                self.message_user(request, f"Usunięto historie cen powiązane z {len(obiekt_ids)} rekordem/rekordami.")

                #usuwaniecie rekordu
                cursor.execute(
                    "DELETE FROM listaSklepow WHERE id IN %s", 
                    [tuple(obiekt_ids)]
                )
                self.message_user(request, f"Usunięto {len(obiekt_ids)} rekord(y) z listy sklepów.")
    usun_rekord.short_description = "Usuń wybrane rekordy (oraz ich historię cen)"
    
    
    #usuwanie sklpeu (wybieramy rekord w ktorym jest nazwa sklepu ktory chcemy usunac, zatweirdzenie usuwa wszsyteki rekordy)
    def usun_sklep(self, request, queryset):
        sklep_nazwa = [obiekty.nazwa for obiekty in queryset]
        
        if not sklep_nazwa:
            self.message_user(request, "Nie wybrano sklepu do usunięcia.", level='error')
            return
        
        #wyszukuje id na podsatwie nazwy
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM listaSklepow WHERE nazwa IN %s", [tuple(sklep_nazwa)])
            sklepy = cursor.fetchall()
        
        if not sklepy:
            self.message_user(request, "Nie znaleziono żadnych sklepów o podanych nazwach.", level='error')
            return
        
        sklepy_ids = [sklep[0] for sklep in sklepy]
        
        with transaction.atomic():
            with connection.cursor() as cursor:
                #usuwanie najpierw z historii cen
                cursor.execute(
                    "DELETE FROM historiacen WHERE id_sklepu_z_danym_produktem IN %s", 
                    [tuple(sklepy_ids)]
                )
                self.message_user(request, f"Usunięto historie cen powiązane z {len(sklepy_ids)} sklepami.")

                #usuwaniecie rekordu
                cursor.execute(
                    "DELETE FROM listaSklepow WHERE id IN %s", 
                    [tuple(sklepy_ids)]
                )
                self.message_user(request, f"Usunięto {len(sklepy_ids)} rekord(y) z listy sklepów.")              
    usun_sklep.short_description = "Usuń sklep"


admin.site.register(ListaSklepow, ListaSklepowAdmin)

