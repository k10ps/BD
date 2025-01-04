from django.db import models
from products.models import ListaProduktow

class ListaOpinii(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_produktu = models.ForeignKey(ListaProduktow, on_delete=models.CASCADE,db_column='id_produktu')
    opinia = models.CharField(max_length=255)
    data = models.DateTimeField()
    
    class Meta:
        managed = False
        db_table = 'listaopinii'

