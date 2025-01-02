from django.contrib import admin
from .models import ListaProduktow

class AdminProdukt(admin.ModelAdmin):
    list_display = ('id','kategoria', 'marka', 'model')

admin.site.register(ListaProduktow, AdminProdukt)