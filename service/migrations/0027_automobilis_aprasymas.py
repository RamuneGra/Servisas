# Generated by Django 4.1.7 on 2023-03-15 09:43

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0026_rename_uzsakovas_uzsakymas_vartotojas'),
    ]

    operations = [
        migrations.AddField(
            model_name='automobilis',
            name='aprasymas',
            field=tinymce.models.HTMLField(default='', verbose_name='Aprašymas'),
        ),
    ]
