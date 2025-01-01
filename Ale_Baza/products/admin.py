from django.contrib import admin
from .models import Listaproduktow

class AdminProdukt(admin.ModelAdmin):
    list_display = ('id','kategoria', 'marka', 'model')

admin.site.register(Listaproduktow, AdminProdukt)