# Generated by Django 5.1.4 on 2025-01-02 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ListaOpinii',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('opinia', models.CharField(max_length=255)),
                ('data', models.DateTimeField()),
            ],
            options={
                'db_table': 'listaopinii',
                'managed': False,
            },
        ),
    ]