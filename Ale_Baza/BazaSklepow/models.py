from django.db import models
from products.models import ListaProduktow

class ListaSklepow(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_produktu = models.ForeignKey(ListaProduktow, on_delete=models.CASCADE,db_column='id_produktu')
    nazwa = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'listasklepow'