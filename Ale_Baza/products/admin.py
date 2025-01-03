from django.contrib import admin
from .models import ListaProduktow
from django.core.exceptions import ValidationError

from django.contrib import admin
from .models import ListaProduktow, Telewizor, Komputer, Monitor, Procesor, Ram

class TelewizorInline(admin.StackedInline):
    model = Telewizor
    extra = 0
    verbose_name = "Specyfikacja dla Telewizora"

class MonitorInline(admin.StackedInline):
    model = Monitor
    extra = 0
    verbose_name = "Specyfikacja dla Monitora"
    
class KomputerInline(admin.StackedInline):
    model = Komputer
    extra = 0
    verbose_name = "Specyfikacja dla Komputera"
    
class ProcesorInline(admin.StackedInline):
    model = Procesor
    extra = 0
    verbose_name = "Procesor (wymagany przy kategorii komputer)"

class RamInline(admin.StackedInline):
    model = Ram
    extra = 0
    verbose_name = "RAM (wymagany przy kategorii komputer)"
    
    
class ListaProduktowAdmin(admin.ModelAdmin):
    list_display=['id', 'kategoria', 'marka', 'model']
    fieldsets = [
        ("Podstawowe informacje o produkcie", {
            'fields': ['kategoria', 'marka', 'model'],
        }),
    ]
    inlines = [TelewizorInline, MonitorInline, KomputerInline, ProcesorInline, RamInline]


admin.site.register(ListaProduktow, ListaProduktowAdmin)

