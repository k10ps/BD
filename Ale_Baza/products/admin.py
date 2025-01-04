from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import ListaProduktow, Telewizor, Komputer, Monitor, Procesor, Ram
from .inline import TelewizorInline, MonitorInline, KomputerInline, ProcesorInline, RamInline


#dodawanie do listaProduktow
class ListaProduktowAdmin(admin.ModelAdmin):
    list_display=['id', 'kategoria', 'marka', 'model']
    
    
    list_filter = ['kategoria', 'marka']
    search_fields = ['kategoria', 'marka', 'model']
    
    #wylaczenie wbudowanego usuwania obiektu w django
    def has_delete_permission(self, request, obj=None):
        return False
    
    fieldsets = [
        ("Podstawowe informacje o produkcie", {'fields': ['kategoria', 'marka', 'model'],}),
    ]
    inlines = [TelewizorInline, MonitorInline, KomputerInline, ProcesorInline, RamInline]

    #delete usuwanie produktu nadpisac action django


admin.site.register(ListaProduktow, ListaProduktowAdmin)

