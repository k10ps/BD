from django.db import models
from products.models import ListaProduktow
from django.core.exceptions import ValidationError

class ListaSklepow(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_produktu = models.ForeignKey(ListaProduktow, on_delete=models.CASCADE,db_column='id_produktu')
    nazwa = models.CharField(max_length=255, verbose_name="Nazwa Sklepu")
    #verbose_name modyfikuje sposob wyswitlania w interfejsie admian
    
    def clean(self):
    #sprawdzanie czy wsyztskie pola uzupełnione
        if not self.id_produktu or not self.nazwa:
            raise ValidationError(f"Uzupełnij dane.")

    class Meta:
        managed = False
        db_table = 'listasklepow'