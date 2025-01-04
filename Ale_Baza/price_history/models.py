from django.db import models
from BazaSklepow.models import ListaSklepow
from django.core.exceptions import ValidationError

class HistoriaCen(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_sklepu_z_danym_produktem = models.ForeignKey(ListaSklepow, on_delete=models.CASCADE,db_column='id_sklepu_z_danym_produktem')
    cena = models.DecimalField(max_digits=8, decimal_places=2)
    data = models.DateField()

    def clean(self):
    #sprawdzanie czy wsyztskie pola uzupełnione
        if not self.id_sklepu_z_danym_produktem or not self.cena or not self.data:
            raise ValidationError(f"Uzupełnij dane.")

    class Meta:
        managed = False
        db_table = 'Historiacen'