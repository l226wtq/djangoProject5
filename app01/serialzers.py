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


class testSerializer(serializers.ModelSerializer):
    sql1 = serializers.SerializerMethodField()

    class Meta:
        model = sqlSingleStatmentList

    def sql1(self):
        qs = sqlSingleStatmentList.objects.filter(sqlID=id, )


class SqlStatementDocumentSerializer(serializers.ModelSerializer):
    # sqls = SqlSingleStatmentListSerializer(many=True, read_only=True)
    # sqls = serializers.PrimaryKeyRelatedField(queryset=sqlSingleStatmentList.objects.all(), many=True)
    # lastSqlStatment = serializers.SerializerMethodField('get_lastSqlStatment')
    # lastsqlExplanation = serializers.SerializerMethodField('get_lastsqlExplanation')
    #
    # def get_lastSqlStatment(self, sql):
    #     qs = sqlSingleStatmentList.objects.filter(sqlID=sql.id).first()
    #     ser = SqlSingleStatmentListSerializer(instance=qs)
    #     # print(ser.data['sqlStatment'])
    #     return ser.data['sqlStatment']
    #
    # def get_lastsqlExplanation(self, sql):
    #     qs = sqlSingleStatmentList.objects.filter(sqlID=sql.id).first()
    #     ser = SqlSingleStatmentListSerializer(instance=qs)
    #     return ser.data['sqlExplanation']

    class Meta:
        model = sqlStatementDocument
        # fields = ('id', 'name', 'sysType', 'type', 'enable', 'lastSqlStatment', 'lastsqlExplanation')
        fields = "__all__"
        # depth=1  # 还可以这么搞

