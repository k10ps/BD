from django.db import models
from django.core.exceptions import ValidationError

# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

class Komputer(models.Model):
    id = models.ForeignKey('ListaProduktow', models.DO_NOTHING, db_column='id', primary_key=True)
    procesor = models.ForeignKey('Procesor', models.DO_NOTHING, db_column='procesor')
    pamiec_ram = models.ForeignKey('Ram', models.DO_NOTHING, db_column='pamiec_RAM')  # Field name made lowercase.
    pojemnosc_dysku = models.IntegerField()

    def clean(self):
    #sprawdzanie czy wsyztskie pola uzupełnione
        if not self.procesor or not self.pamiec_ram or not self.pojemnosc_dysku:
            raise ValidationError(f"Uzupełnij specyfikacje komputera.")
        
    class Meta:
        managed = False
        db_table = 'komputer'


class ListaProduktow(models.Model):
    id = models.BigAutoField(primary_key=True)
    kategoria = models.CharField(max_length=255)
    marka = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    
    def clean(self):
        dozwolone_kategorie = ['telewizor', 'komputer', 'monitor', 'procesor', 'ram']
        #sprawdzanie czy kategoria dozwolona
        if self.kategoria.lower() not in dozwolone_kategorie:
            raise ValidationError(f"Kategoria '{self.kategoria}' jest nieprawidłowa, produkt może należeć tylko do kategorii telewizor/komputer/monitor/procesor/ram.")

        #sprawdzanie czy wsyztskie pola uzupełnione
        if not self.kategoria or not self.marka or not self.model:
            raise ValidationError(f"Uzupełnij wszystkie pola.")
    class Meta:
        managed = False
        db_table = 'ListaProduktow'


class Monitor(models.Model):
    id = models.ForeignKey(ListaProduktow, models.DO_NOTHING, db_column='id', primary_key=True)
    przekatna_cal_field = models.IntegerField(db_column='przekatna_(cal)')  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    odswiezanie_hz_field = models.IntegerField(db_column='odswiezanie_(Hz)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    rozdzielczosc = models.BigIntegerField(db_column='rozdzielczość')
    typ_wyswietlacza = models.CharField(max_length=255)
    glosniki_field = models.IntegerField(db_column='glosniki_')  # Field renamed because it ended with '_'.
    proporcje_ekranu = models.CharField(max_length=255)

    def clean(self):
        if not self.przekatna_cal_field or not self.odswiezanie_hz_field or not self.rozdzielczosc or not self.typ_wyswietlacza or not self.glosniki_field or not self.proporcje_ekranu:
            raise ValidationError(f"Uzupełnij specyfikacje monitora.")
    class Meta:
        managed = False
        db_table = 'monitor'


class Procesor(models.Model):
    id = models.ForeignKey(ListaProduktow, models.DO_NOTHING, db_column='id', primary_key=True)
    liczba_rdzeni = models.BigIntegerField()
    taktowanie = models.BigIntegerField()
    rodzaj_gniazda = models.CharField(max_length=255)

    def clean(self):
        if not self.liczba_rdzeni or not self.taktowanie or not self.rodzaj_gniazda:
            raise ValidationError(f"Uzupełnij specyfikacje procesora.")        
    class Meta:
        managed = False
        db_table = 'procesor'


class Ram(models.Model):
    id = models.ForeignKey(ListaProduktow, models.DO_NOTHING, db_column='id', primary_key=True)
    typ_pamieci = models.CharField(max_length=255)
    pojemnosc_gb_field = models.IntegerField(db_column='pojemnosc_(GB)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    taktowanie_mhz_field = models.BigIntegerField(db_column='taktowanie_(MHz)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    def clean(self):
        if not self.typ_pamieci or not self.pojemnosc_gb_field or not self.taktowanie_mhz_field:
            raise ValidationError(f"Uzupełnij specyfikacje RAMu.")            
    class Meta:
        managed = False
        db_table = 'ram'


class Telewizor(models.Model):
    id = models.ForeignKey(ListaProduktow, models.DO_NOTHING, db_column='id', primary_key=True)
    przekatna_cal_field = models.IntegerField(db_column='przekatna_(cal)')  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    typ_wyswietlacza = models.CharField(max_length=255)
    rozdzielczosc_xk_field = models.BigIntegerField(db_column='rozdzielczosc_(xK)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    smart_tv = models.IntegerField(db_column='smart_TV')  # Field name made lowercase.

    def clean(self):
        if not self.przekatna_cal_field or not self.typ_wyswietlacza or not self.rozdzielczosc_xk_field or not self.smart_tv:
            raise ValidationError(f"Uzupełnij specyfikacje telewizora.")
    class Meta:
        managed = False
        db_table = 'telewizor'
