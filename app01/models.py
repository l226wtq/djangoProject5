from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=500, verbose_name="标题", blank=True)
    author = models.CharField(max_length=100, verbose_name="作者", blank=True)
    publishDate = models.DateField(auto_now=False, auto_now_add=False, verbose_name="发行时间", blank=True, null=True)
    rating = models.SmallIntegerField(verbose_name="评分", blank=True, null=True)
    type = models.CharField(max_length=200, verbose_name="种类", blank=True)


class GoodsInventory(models.Model):
    number = models.CharField(max_length=10, verbose_name="货品编号")
    type = models.CharField(max_length=50, verbose_name="货品类别")
    name = models.CharField(max_length=500, verbose_name="货品名称")
    specification = models.CharField(max_length=50, verbose_name="规格型号")
    unit = models.CharField(max_length=10, verbose_name="单位")
    inventoryQuantity = models.PositiveIntegerField(verbose_name="库存数量", default=0)


class GoodsList(models.Model):
    type = models.CharField(max_length=50, verbose_name="货品类别")
    number = models.CharField(max_length=10, verbose_name="货品编号")
    name = models.CharField(max_length=500, verbose_name="货品名称")
    specification = models.CharField(max_length=50, verbose_name="规格型号")
    unit = models.CharField(max_length=10, verbose_name="单位")
    pic = models.CharField(max_length=500, verbose_name="货品图片")
    purchasePrice = models.PositiveIntegerField(verbose_name="参考进价", default=0)
    sellingPrice = models.PositiveIntegerField(verbose_name="参考售价", default=0)
    minInventoryQuantity = models.PositiveIntegerField(verbose_name="库存数量", default=0)
    maxInventoryQuantity = models.PositiveIntegerField(verbose_name="库存数量", default=0)
    remark = models.CharField(max_length=200, verbose_name="参考进价")


class BoundJournalList(models.Model):
    date = models.DateTimeField(verbose_name="业务日期")
    journalType = models.CharField(max_length=20, verbose_name="单据类型")
    journalNumber = models.CharField(max_length=60, verbose_name="单据编号")
    number = models.CharField(max_length=10, verbose_name="货品编号")
    type = models.CharField(max_length=50, verbose_name="货品类别")
    name = models.CharField(max_length=500, verbose_name="货品名称")
    specification = models.CharField(max_length=50, verbose_name="规格型号")
    unit = models.CharField(max_length=10, verbose_name="单位")
    inboundCount = models.PositiveIntegerField(verbose_name="入库数量", null=True, blank=True)
    inboundAmount = models.PositiveIntegerField(verbose_name="入库金额", null=True, blank=True)
    outboundCount = models.PositiveIntegerField(verbose_name="出库数量", null=True, blank=True)
    outboundAmount = models.PositiveIntegerField(verbose_name="出库金额", null=True, blank=True)


class sqlStatementDocument(models.Model):
    class sqlType(models.TextChoices):
        SEARCH = 'sear', 'search'
        UPDATE = 'up', 'update'
        ADD = 'a', 'add'
        REMOVE = 'rem', 'remove'

    class sysTypeName(models.TextChoices):
        RENSHI = 'renshi', 'renshi'
        XIAOSHOU = 'xiaoshou', 'xiaoshou'
        KAOQING = 'kaoqing', 'kaoqing'

    name = models.CharField(max_length=200, verbose_name="SQL语句名称")
    sysType = models.CharField(max_length=200, verbose_name="SQL所属系统", choices=sysTypeName.choices,
                               default=sysTypeName.RENSHI)
    type = models.CharField(choices=sqlType.choices, default=sqlType.SEARCH, max_length=10, verbose_name="SQL操作类型")
    enable = models.BooleanField(verbose_name="启用状态")
    sqlStatment = models.TextField(verbose_name="SQL语句")
    sqlExplanation = models.TextField(verbose_name="SQL注释说明")


class sqlSingleStatmentList(models.Model):
    sqlStatment = models.TextField(verbose_name="SQL语句")
    sqlExplanation = models.TextField(verbose_name="SQL注释说明")
    author = models.CharField(max_length=100, verbose_name="作者", default="未知作者")
    sqlID = models.ForeignKey('sqlStatementDocument', on_delete=models.CASCADE)
