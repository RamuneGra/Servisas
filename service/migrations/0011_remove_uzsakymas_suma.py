# Generated by Django 4.1.7 on 2023-03-08 08:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0010_remove_uzsakymoeilute_kaina'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uzsakymas',
            name='suma',
        ),
    ]
