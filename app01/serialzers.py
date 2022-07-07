from rest_framework import serializers

# Serializers define the API representation.
from app01.models import Book, GoodsInventory, GoodsList, BoundJournalList, sqlStatementDocument, sqlSingleStatmentList


#
class BookInfoSerializer(serializers.ModelSerializer):
    # 定义序列化
    class Meta:
        model = Book  # 定义序列化器需要映射的字段
        fields = '__all__'  # 映射模型的哪些字段


# class BookInfoSerializer(serializers.ModelSerializer):
#     # 定义序列化器
#     class Meta:
#         model=Book
#
#         id = serializers.IntegerField(label='ID', read_only=True)
#         title = serializers.CharField(label="标题", required=False)
#         publishDate = serializers.DateTimeField(label='出版时间', required=False)
#         rating = serializers.IntegerField(label='评分', required=False)
#         type = serializers.CharField(label='种类', required=False)
class GoodsInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsInventory
        fields = "__all__"


class GoodsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsList
        fields = "__all__"


class BoundJournalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoundJournalList
        fields = "__all__"


class SqlSingleStatmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = sqlSingleStatmentList
        # fields = ('author', 'sqlStatment', 'sqlExplanation', 'id', 'sqlID')
        fields = "__all__"


class SqlStatementDocumentSerializer(serializers.ModelSerializer):
    # sqls = SqlSingleStatmentListSerializer(many=True, read_only=True)
    class Meta:
        model = sqlStatementDocument
        fields = ('id', 'name', 'sysType', 'type', 'enable', 'sqls1')

        depth=1  # 还可以这么搞