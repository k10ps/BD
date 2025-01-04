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
    verbose_name = "Specyfikacja Procesora"

class RamInline(admin.StackedInline):
    model = Ram
    extra = 0
    verbose_name = "Specyfikacja RAMu"