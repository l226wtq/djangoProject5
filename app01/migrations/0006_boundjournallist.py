# Generated by Django 4.0.4 on 2022-06-15 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_goodslist'),
    ]

    operations = [
        migrations.CreateModel(
            name='boundJournalList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='业务类型')),
                ('journalType', models.CharField(max_length=50, verbose_name='单据类型')),
                ('journalNumber', models.CharField(max_length=10, verbose_name='单据编号')),
                ('number', models.CharField(max_length=10, verbose_name='货品编号')),
                ('type', models.CharField(max_length=50, verbose_name='货品类别')),
                ('name', models.CharField(max_length=500, verbose_name='货品名称')),
                ('specification', models.CharField(max_length=50, verbose_name='规格型号')),
                ('unit', models.CharField(max_length=10, verbose_name='单位')),
                ('inboundCount', models.PositiveIntegerField(default=0, verbose_name='入库数量')),
                ('inboundAmount', models.PositiveIntegerField(default=0, verbose_name='入库金额')),
                ('outboundCount', models.PositiveIntegerField(default=0, verbose_name='出库数量')),
                ('outboundAmount', models.PositiveIntegerField(default=0, verbose_name='出库金额')),
            ],
        ),
    ]
