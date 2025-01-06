from django.contrib import admin, messages
from django.db import connection
from django.core.exceptions import ValidationError
from .models import HistoriaCen
#do zainstalowania pozwala wybrac zakres na ktorym chcemy przeszukiwac
from django.contrib.admin import SimpleListFilter

class CenaRangeFilter(SimpleListFilter):
    title = 'Zakres cen'
    parameter_name = 'cena_range'

    def lookups(self, request, model_admin):
        return [
            ('0-500', '0 - 500'),
            ('500-1000', '500 - 1000'),
            ('1000-2000', '1000 - 2000'),
            ('2000-5000', '2000 - 5000'),
            ('5000+', '5000+'),
        ]

    def queryset(self, request, queryset):
        if self.value() == '0-500':
            return queryset.filter(cena__gte=0, cena__lte=500)
        elif self.value() == '500-1000':
            return queryset.filter(cena__gte=500, cena__lte=1000)
        elif self.value() == '1000-2000':
            return queryset.filter(cena__gte=1000, cena__lte=2000)
        elif self.value() == '2000-5000':
            return queryset.filter(cena__gte=2000, cena__lte=4999)
        elif self.value() == '5000+':
            return queryset.filter(cena__gte=5000)
        return queryset

class HistoriaCenAdmin(admin.ModelAdmin):
    list_display=['id', 'wys_id_sklepu_z_danym_produktem', 'cena', 'data']
    list_filter = [CenaRangeFilter, 'data']
    search_fields = ['cena', 'data']
    
    actions=['usun_cene']
    
    #wylaczenie wbudowanego usuwania obiektu w django
    def has_delete_permission(self, request, obj=None):
        return False
    
    #modyfikuje wyswitlanie id_sklepu_z_danym_produktem, wcześniej 'ListaSklepow object(2)', teraz '2'
    def wys_id_sklepu_z_danym_produktem(self, obj):
        return obj.id_sklepu_z_danym_produktem.id
    wys_id_sklepu_z_danym_produktem.short_description = "ID SKLEPU Z DANYM PRODUKTEM"
    
   
    def save_model(self, request, obj, form, change):
        try:
            with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO historiacen (id_sklepu_z_danym_produktem, cena, data) VALUES (%s, %s, %s)",
                        [obj.id_sklepu_z_danym_produktem.id, obj.cena, obj.data]
                    )
            messages.success(request, f"Historia cen produktu: '{obj.id_sklepu_z_danym_produktem}' została pomyślnie dodana.")
        except Exception as e:
            # Obsługa błędów
            messages.error(request, f"Błąd podczas dodawania.")
    
    #usuwanie rekordu
    def usun_cene(self, request, queryset):
        historia_ids = [historia.id for historia in queryset]
        if historia_ids:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM historiacen WHERE id IN %s", [tuple(historia_ids)])
            messages.success(request, f"Usunięto {len(historia_ids)} element z historii cen.")
        else:
            messages.error(request, "Nie wybrano obiektu do usuniecia.", level='error')
    usun_cene.short_description = "Usun element"
    
    
admin.site.register(HistoriaCen, HistoriaCenAdmin)
    
