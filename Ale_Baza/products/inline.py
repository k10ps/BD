from django.contrib import admin
from .models import ListaProduktow, Telewizor, Komputer, Monitor

class TelewizorInline(admin.StackedInline):
    model = Telewizor
    extra = 0

class KomputerInline(admin.StackedInline):
    model = Komputer
    extra = 0

class MonitorInline(admin.StackedInline):
    model = Monitor
    extra = 0
