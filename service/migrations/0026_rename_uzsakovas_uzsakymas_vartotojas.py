# Generated by Django 4.1.7 on 2023-03-15 08:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0025_alter_uzsakymas_terminas'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uzsakymas',
            old_name='uzsakovas',
            new_name='vartotojas',
        ),
    ]
