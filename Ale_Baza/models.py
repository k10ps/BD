# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Historiacen(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_sklepu_z_danym_produktem = models.ForeignKey('Listasklepow', models.DO_NOTHING, db_column='id_sklepu_z_danym_produktem')
    cena = models.DecimalField(max_digits=8, decimal_places=2)
    data = models.DateField()

    class Meta:
        managed = False
        db_table = 'historiacen'


class Komputer(models.Model):
    id = models.ForeignKey('Listaproduktow', models.DO_NOTHING, db_column='id', primary_key=True)
    procesor = models.ForeignKey('Procesor', models.DO_NOTHING, db_column='procesor')
    pamiec_ram = models.ForeignKey('Ram', models.DO_NOTHING, db_column='pamiec_RAM')  # Field name made lowercase.
    pojemnosc_dysku = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'komputer'


class Listaopinii(models.Model):
    id = models.BigIntegerField(primary_key=True)
    id_produktu = models.BigIntegerField()
    opinia = models.CharField(max_length=255)
    data = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'listaopinii'


class Listaproduktow(models.Model):
    id = models.BigAutoField(primary_key=True)
    kategoria = models.CharField(max_length=255)
    marka = models.CharField(max_length=255)
    model = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'listaproduktow'


class Listasklepow(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_produktu = models.BigIntegerField()
    nazwa = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'listasklepow'


class Monitor(models.Model):
    id = models.ForeignKey(Listaproduktow, models.DO_NOTHING, db_column='id', primary_key=True)
    przekatna_cal_field = models.IntegerField(db_column='przekatna_(cal)')  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    odswiezanie_hz_field = models.IntegerField(db_column='odswiezanie_(Hz)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    rozdzielczoťŠ = models.BigIntegerField()
    typ_wyswietlacza = models.CharField(max_length=255)
    glosniki_field = models.IntegerField(db_column='glosniki_')  # Field renamed because it ended with '_'.
    proporcje_ekranu = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'monitor'


class Procesor(models.Model):
    id = models.ForeignKey(Listaproduktow, models.DO_NOTHING, db_column='id', primary_key=True)
    liczba_rdzeni = models.BigIntegerField()
    taktowanie = models.BigIntegerField()
    rodzaj_gniazda = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'procesor'


class Ram(models.Model):
    id = models.ForeignKey(Listaproduktow, models.DO_NOTHING, db_column='id', primary_key=True)
    typ_pamieci = models.CharField(max_length=255)
    pojemnosc_gb_field = models.IntegerField(db_column='pojemnosc_(GB)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    taktowanie_mhz_field = models.BigIntegerField(db_column='taktowanie_(MHz)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.

    class Meta:
        managed = False
        db_table = 'ram'


class Telewizor(models.Model):
    id = models.ForeignKey(Listaproduktow, models.DO_NOTHING, db_column='id', primary_key=True)
    przekatna_cal_field = models.IntegerField(db_column='przekatna_(cal)')  # Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    typ_wyswietlacza = models.CharField(max_length=255)
    rozdzielczosc_xk_field = models.BigIntegerField(db_column='rozdzielczosc_(xK)')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it ended with '_'.
    smart_tv = models.IntegerField(db_column='smart_TV')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'telewizor'
