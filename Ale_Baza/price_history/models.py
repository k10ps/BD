from django.db import models
from BazaSklepow.models import ListaSklepow

class HistoriaCen(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_sklepu_z_danym_produktem = models.ForeignKey(ListaSklepow, on_delete=models.CASCADE,db_column='id_sklepu_z_danym_produktem')
    cena = models.DecimalField(max_digits=8, decimal_places=2)
    data = models.DateField()

    class Meta:
        managed = False
        db_table = 'Historiacen'