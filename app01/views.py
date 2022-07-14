from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, \
    RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet, GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework import status

from BaseOrm import DictToModel
from app01.models import Book, GoodsInventory, GoodsList, BoundJournalList, sqlStatementDocument, sqlSingleStatmentList
from django.utils import timezone
# from app01.forms import newSqlForm
import json
import zipfile
import os

from rest_framework import routers, serializers, viewsets

# Create your views here.
from app01.serialzers import BookInfoSerializer, GoodsInventorySerializer, GoodsListSerializer, \
    BoundJournalListSerializer, SqlStatementDocumentSerializer, SqlSingleStatmentListSerializer


class BookInfoView(ModelViewSet):  # 包含全部的Mixin类
    # 定义类视图
    # 指定查询集
    queryset = Book.objects.all()
    # 指定序列化器
    serializer_class = BookInfoSerializer


class BookInfoApiView(APIView):
    # 列表视图
    def get(self, request):
        books = Book.objects.all()
        ser = BookInfoSerializer(instance=books, many=True)
        return Response(ser.data)

    def post(self, request):
        # 获取前端发过来的数据并且反序列化
        ser = BookInfoSerializer(data=request.data)
        # 验证数据并抛出异常
        ser.is_valid(raise_exception=True)
        # 序列化器save方法执行create方法
        ser.save()
        # 返回新增的数据
        return Response(ser.data, status=status.HTTP_201_CREATED)


class BookInfoSingleApiView(APIView):
    def get(self, request, pk):
        book = Book.objects.get(id=pk)
        ser = BookInfoSerializer(book)
        return Response(ser.data)

    def put(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ser = BookInfoSerializer(instance=book, data=request.data)
        ser.is_valid(raise_exception=True)
        ser.save()
        return Response(ser.data, status=status.HTTP_200_OK)

    def delete(self, reuqest, pk):
        try:
            book = Book.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookInfoGenericApiView(ListCreateAPIView):
    # 指定序列化器
    serializer_class = BookInfoSerializer
    # 指定查询集，即数据来源
    queryset = Book.objects.all()

    # 甚至还有ListCreateAPIView，不用在内部多继承
    # 因为继承了ListAPIView
    # def get(self, request):
    #     #     qs = self.get_queryset()
    #     #     ser = self.get_serializer(qs, many=True)
    #     #     return Response(ser.data)
    #     return self.list(request)
    # 因为继承了CreateAPIView
    # def post(self, request):
    #     return self.create(request)


class BookInfoSingleGenericApiView(RetrieveUpdateDestroyAPIView):
    # 指定序列化器
    serializer_class = BookInfoSerializer
    # 指定查询集，即数据来源
    queryset = Book.objects.all()

    # def get(self, request, pk):
    #     # book = self.get_object()  # 不用传入id
    #     # ser = self.get_serializer(book)
    #     # return Response(ser.data)
    #     return self.retrieve(request)
    #
    # def put(self, request, pk):
    #     # book = self.get_object()
    #     # ser = self.get_serializer(book, request.data)
    #     # ser.is_valid(raise_exception=True)
    #     # ser.save()
    #     # return Response(ser.data)
    #     return self.update(request)


def getBookPicFileName(obj):
    return int(os.path.splitext(obj.filename)[0])


class BookInfoSingleZip(ViewSet):

    def picLength(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ser = BookInfoSerializer(book)
        # print(ser.data['title'])
        bookTitle = ser.data['title']
        bookPath=ser.data['path']
        if os.path.exists(f'''{bookPath}//{bookTitle}.zip'''):
            bookZip = zipfile.ZipFile(f'''{bookPath}//{bookTitle}.zip''', mode="r")
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        # print([item for item in bookZip.infolist() if not item.is_dir()])
        return HttpResponse([item for item in bookZip.infolist() if not item.is_dir()].__len__())
        # for item in bookZip.infolist():
        #     if item.is_dir():
        #         continue
        #     else:
        #         file = bookZip.read(item)
        #         return HttpResponse(file, content_type='image/jpg')

    def bookPic(self, request, pk, page):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ser = BookInfoSerializer(book)
        bookTitle = ser.data['title']
        bookPath=ser.data['path']
        # picHeight=request.query_params['height']
        # picWidth=request.query_params['width']
        if os.path.exists(f'''{bookPath}//{bookTitle}.zip'''):
            bookZip = zipfile.ZipFile(f'''{bookPath}//{bookTitle}.zip''', mode="r")
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        templist=[item for item in bookZip.infolist() if not item.is_dir()]
        templist.sort(key=getBookPicFileName)  # 按照数字名称排序
        print(templist)
        # picList = [item for item in bookZip.infolist() if not item.is_dir()].sort()
        # return HttpResponse(bookZip.read(picList[page - 1]), content_type='image/webp')
        return HttpResponse(bookZip.read(templist[page - 1]), content_type='image/webp')


class BookInfoAPIViewSet(ViewSet):
    def list(self, request):
        books = Book.objects.all()
        ser = BookInfoSerializer(books, many=True)
        return Response(ser.data)

    def retrieve(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        ser = BookInfoSerializer(book)
        return Response(ser.data)


class BookCoverApiView(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


# class BookInfoGenericApiViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin):  # 全靠指定Mixin就能使用简单的协议方法
class BookInfoGenericApiViewSet(ReadOnlyModelViewSet):  # 整合到一个类中继承
    serializer_class = BookInfoSerializer
    queryset = Book.objects.all()


class GoodsIntentoryListGenericApiViewSet(ReadOnlyModelViewSet):
    serializer_class = GoodsInventorySerializer
    queryset = GoodsInventory.objects.all()


class GoodsListGenericApiViewSet(ReadOnlyModelViewSet):
    serializer_class = GoodsListSerializer
    queryset = GoodsList.objects.all()


class GoodsListNumsListGenericApi(GenericAPIView):
    serializer_class = GoodsListSerializer
    queryset = GoodsList.objects.all()

    def get(self, request):
        qs = self.get_queryset()
        ser = self.get_serializer(qs, many=True)
        numList = []
        for dic in ser.data:
            numList.append(dic['number'])
        return Response(numList)


class BoundJournalListGenericApiViewSet(ModelViewSet):
    serializer_class = BoundJournalListSerializer
    queryset = BoundJournalList.objects.all()


class sqlStatementDocumentGenericApiViewSet(ModelViewSet):
    serializer_class = SqlStatementDocumentSerializer
    queryset = sqlStatementDocument.objects.all()

    # def list(self, request, *args, **kwargs):
    #     queryset = sqlStatementDocument.objects.all()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     sqlSingleStatmentList.objects.create(sqlStatment=request.data['lastSqlStatment'],
    #                                          sqlExplanation=request.data['lastsqlExplanation'],
    #                                          author='lyyTest',
    #                                          sqlID=sqlStatementDocument.objects.get(id=serializer.data['id']))
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # form = newSqlForm(request.data)
    # sqlSingleStatmentList.objects.create(
    #     sqlID=sqlStatementDocument.objects.create(name='测试2', sysType="x", type="a", enable=True),
    #     sqlStatment="select * from", sqlExplanation="x", author="x")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        sqlSingleStatmentList.objects.create(sqlStatment=request.data['lastestSqlStatment'],
                                             sqlExplanation=request.data['lastestSqlExplanation'],
                                             sqlID=sqlStatementDocument.objects.get(id=serializer.data['id']))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    # def allsingleStatments(self, request):
    #     # queryset = sqlStatementDocument.objects.all()
    #     # ser = SqlStatementDocumentSerializer(queryset, many=True)
    #     # # print(queryset.author)
    #     # return Response(ser.data)
    #     # queryset = sqlStatementDocument.objects.all()
    #     form = newSqlForm(request.data)
    def retrieve(self, request, *args, **kwargs):
        qs = sqlSingleStatmentList.objects.filter(sqlID=kwargs['pk']).all()
        ser = SqlSingleStatmentListSerializer(qs, many=True)
        return Response(ser.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # print(instance.name, instance.lastestSqlStatment, instance.lastestSqlExplanation)
        if (request.data['lastestSqlStatment'] != instance.lastestSqlStatment or request.data[
            'lastestSqlExplanation'] != instance.lastestSqlExplanation):
            print('有修改')
            sqlSingleStatmentList.objects.create(sqlStatment=request.data['lastestSqlStatment'],
                                                 sqlExplanation=request.data['lastestSqlExplanation'],
                                                 sqlID=sqlStatementDocument.objects.get(id=instance.id))

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()


class sqlSingleStatmentListApiViewSet(ModelViewSet):
    serializer_class = SqlSingleStatmentListSerializer
    queryset = sqlSingleStatmentList.objects.all()


def getAllBooksInfo(request):
    jsonList = []
    for item in Book.objects.all():
        tempDic = {}
        tempDic["id"] = item.id
        tempDic["title"] = item.title
        tempDic["author"] = item.author
        tempDic["publishDate"] = "2022-05-27"
        tempDic["rating"] = item.rating
        tempDic['type'] = item.type
        jsonList.append(tempDic)
    print(jsonList)
    jsonTemp = json.dumps(jsonList, ensure_ascii=False)
    return JsonResponse(jsonTemp, safe=False)


def addOneRowBookInfo(request):
    print(request.body)
    rowJsonDic = json.loads(request.body)
    tempRow = Book(title=rowJsonDic["title"], author=rowJsonDic["author"], publishDate=rowJsonDic["publishDate"],
                   rating=rowJsonDic["rating"],
                   type=rowJsonDic["type"])
    tempRow.save()
    return JsonResponse({"code": 0})


def deleteOneRowBookInfo(request):
    delid = request.GET.get('delRowid')
    Book.objects.filter(id=delid).delete()
    return JsonResponse({"code": 0})


def updateOneRowBookInfo(request):
    updateRow = request.GET.get("updateRowId")
    updateInfo = json.loads(request.body)
    # updateRow = Book(id=updateInfo["id"], title=updateInfo["title"], author=updateInfo["author"],
    #                  publishDate=timezone.now(),
    #                  rating=updateInfo["rating"],
    #                  type=updateInfo["type"])
    obj = {"id": updateRow}

    updateRowObject = Book.objects.get(id=updateRow)
    a = DictToModel(updateInfo, Book)
    s: Book = a.format_dict_data_to_model()
    print(s.author)

    # a = updateRowObject(**updateInfo)
    # updateRowObject(author=updateInfo['author'])

    #     updateRowObject.keys=values
    # updateName=updateInfo[0]["data"].keys()
    # updateRow.save(updateInfo[0]["data"])
    # updateRowObject.save()
    return JsonResponse({"code": 0})
