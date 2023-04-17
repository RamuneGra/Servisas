# Generated by Django 4.1.7 on 2023-03-07 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0006_alter_uzsakymas_suma_alter_uzsakymoeilute_kaina'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paslauga',
            name='paslaugos_kaina',
            field=models.DecimalField(decimal_places=2, help_text='Įveskite paslaugos kainą', max_digits=8, verbose_name='Kaina'),
        ),
    ]
