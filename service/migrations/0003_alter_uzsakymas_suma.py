# Generated by Django 4.1.7 on 2023-03-07 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0002_remove_uzsakymoeilute_kaina_alter_uzsakymas_suma'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uzsakymas',
            name='suma',
            field=models.FloatField(blank=True, null=True, verbose_name='Suma'),
        ),
    ]
