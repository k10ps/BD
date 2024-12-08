from django.db import models

# Create your models here.
from django.db import models

class Lista_produktow(models.Model):
    id = models.BigAutoField(primary_key=True)
    kategoria = models.CharField(max_length=255)
    marka = models.CharField(max_length=255)
    model = models.CharField(max_length=255)

    class Meta:
        db_table = 'Lista_produktow'

class Telewizor(models.Model):
    id = models.OneToOneField(Lista_produktow, on_delete=models.CASCADE, primary_key=True)
    przekatna_cal = models.IntegerField()
    typ_wyswietlacza = models.CharField(max_length=255)
    rozdzielczosc_xK = models.BigIntegerField()
    smart_TV = models.BooleanField()

    class Meta:
        db_table = 'Telwizor'

class Komputer(models.Model):
    id = models.OneToOneField(Lista_produktow, on_delete=models.CASCADE, primary_key=True)
    procesor = models.ForeignKey('Procesor', on_delete=models.CASCADE)
    pamiec_RAM = models.ForeignKey('RAM', on_delete=models.CASCADE)
    pojemnosc_dysku = models.IntegerField()

    class Meta:
        db_table = 'Komputer'

class Monitor(models.Model):
    id = models.OneToOneField(Lista_produktow, on_delete=models.CASCADE, primary_key=True)
    przekatna_cal = models.IntegerField()
    odswiezanie_Hz = models.IntegerField()
    rozdzielczosc = models.BigIntegerField()
    typ_wyswietlacza = models.CharField(max_length=255)
    glosniki = models.BooleanField()
    proporcje_ekranu = models.CharField(max_length=255)

    class Meta:
        db_table = 'Monitor'

class Procesor(models.Model):
    id = models.OneToOneField(Lista_produktow, on_delete=models.CASCADE, primary_key=True)
    liczba_rdzeni = models.BigIntegerField()
    taktowanie = models.BigIntegerField()
    rodzaj_gniazda = models.CharField(max_length=255)

    class Meta:
        db_table = 'Procesor'

class RAM(models.Model):
    id = models.OneToOneField(Lista_produktow, on_delete=models.CASCADE, primary_key=True)
    typ_pamieci = models.CharField(max_length=255)
    pojemnosc_GB = models.IntegerField()
    taktowanie_MHz = models.BigIntegerField()

    class Meta:
        db_table = 'RAM'

class Lista_sklepow(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_produktu = models.ForeignKey(Lista_produktow, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=255)

    class Meta:
        db_table = 'Lista_sklepow'

class Historia_cen(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_sklepu_z_danym_produktem = models.ForeignKey(Lista_sklepow, on_delete=models.CASCADE)
    cena = models.DecimalField(max_digits=8, decimal_places=2)
    data = models.DateField()

    class Meta:
        db_table = 'Historia_cen'

    class Meta:
        unique_together = ('id',)

class Lista_opinii(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_produktu = models.ForeignKey(Lista_produktow, on_delete=models.CASCADE)
    opinia = models.CharField(max_length=255)
    data = models.DateTimeField()

    class Meta:
        db_table = 'Lista_opinii'

    class Meta:
        unique_together = ('id',)

