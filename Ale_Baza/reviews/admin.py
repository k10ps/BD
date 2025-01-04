from django.contrib import admin
from django.db import connection
from django.core.exceptions import ValidationError
from .models import ListaOpinii


class ListaOpiniiAdmin(admin.ModelAdmin):
    list_display=['id', 'display_id_produktu', 'opinia', 'data']
    actions=['usun_opinie']
    
    list_filter = ['data']
    search_fields = ['id_produktu__id', 'opinia', 'data']
    
    def display_id_produktu(self, obj):
        return obj.id_produktu.id
    display_id_produktu.short_description = "ID Produktu"
    
    #zablokowanie mozliwsoci dodawania opinii u admina
    def has_add_permission(self, request):
        return False
    #wylaczenie wbudowanego usuwania obiektu w django
    def has_delete_permission(self, request, obj=None):
        return False
    
    #usuwanie opinii
    def usun_opinie(self, request, queryset):
        opinion_ids = [opinion.id for opinion in queryset]
        if opinion_ids:
            with connection.cursor() as cursor:
                
                cursor.execute("DELETE FROM listaopinii WHERE id IN %s", [tuple(opinion_ids)])
            self.message_user(request, f"Usunięto {len(opinion_ids)} opinii.")
        else:
            self.message_user(request, "Nie wybrano opinii do usunięcia.", level='error')
    usun_opinie.short_description = "Usun wybrane opinie"

admin.site.register(ListaOpinii, ListaOpiniiAdmin)

