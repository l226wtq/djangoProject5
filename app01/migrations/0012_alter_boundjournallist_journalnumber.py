# Generated by Django 4.0.4 on 2022-06-17 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0011_alter_boundjournallist_journalnumber_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boundjournallist',
            name='journalNumber',
            field=models.CharField(max_length=60, verbose_name='单据编号'),
        ),
    ]
