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
from app01.models import Book, GoodsInventory, GoodsList, BoundJournalList, sqlStatementDocument
from django.utils import timezone
import json
import zipfile
import os

from rest_framework import routers, serializers, viewsets

# Create your views here.
from app01.serialzers import BookInfoSerializer, GoodsInventorySerializer, GoodsListSerializer, \
    BoundJournalListSerializer, SqlStatementDocumentSerializer


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


class BookInfoSingleZip(ViewSet):

    def picLength(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        ser = BookInfoSerializer(book)
        # print(ser.data['title'])
        bookTitle = ser.data['title']
        if os.path.exists(f'''./app01/static/bookZips/{bookTitle}.zip'''):
            bookZip = zipfile.ZipFile(f'''./app01/static/bookZips/{bookTitle}.zip''', mode="r")
        else:
            return Response(status.HTTP_404_NOT_FOUND)
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
            return Response(status.HTTP_404_NOT_FOUND)
        ser = BookInfoSerializer(book)
        bookTitle = ser.data['title']
        # picHeight=request.query_params['height']
        # picWidth=request.query_params['width']
        if os.path.exists(f'''./app01/static/bookZips/{bookTitle}.zip'''):
            bookZip = zipfile.ZipFile(f'''./app01/static/bookZips/{bookTitle}.zip''', mode="r")
        else:
            return Response(status.HTTP_404_NOT_FOUND)
        # print([item for item in bookZip.infolist() if not item.is_dir()])
        picList = [item for item in bookZip.infolist() if not item.is_dir()]
        return HttpResponse(bookZip.read(picList[page - 1]), content_type='image/jpg')


class BookInfoAPIViewSet(ViewSet):
    def list(self, request):
        books = Book.objects.all()
        ser = BookInfoSerializer(books, many=True)
        return Response(ser.data)

    def retrieve(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        ser = BookInfoSerializer(book)
        return Response(ser.data)


class BookCoverApiView(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
        except Book.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)


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

    def list(self, request, *args, **kwargs):
        if kwargs.get('sysType') == 'renshi':
            queryset = self.filter_queryset(self.get_queryset().filter(sysType='renshi'))

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        else:
            return super().list(request, *args, **kwargs)


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
