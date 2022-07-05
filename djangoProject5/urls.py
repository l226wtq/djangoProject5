"""djangoProject5 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app01 import views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
    path("getAllBooksInfo/", views.getAllBooksInfo),
    path("addOneRowBookInfo/", views.addOneRowBookInfo),
    path("deleteOneRowBookInfo/", views.deleteOneRowBookInfo),
    path("updateOneRowBookInfo/", views.updateOneRowBookInfo),
    path("book/", views.BookInfoApiView.as_view()),
    path("book/<int:pk>/", views.BookInfoSingleApiView.as_view()),
    path("genericbook/", views.BookInfoGenericApiView.as_view()),
    path("genericbook/<int:pk>/", views.BookInfoSingleGenericApiView.as_view()),
    path("genericbook/zip/<int:pk>/", views.BookInfoSingleZip.as_view({'get': 'picLength'})),
    path("genericbook/zip/<int:pk>&page=<int:page>/", views.BookInfoSingleZip.as_view({'get': 'bookPic'})),
    path("viewsetbook/", views.BookInfoAPIViewSet.as_view({'get': 'list'})),
    path("viewsetbook/<int:pk>/", views.BookInfoAPIViewSet.as_view({'get': 'retrieve'})),
    path("genericviewsetbook/", views.BookInfoGenericApiViewSet.as_view({'get': 'list'})),
    path("genericviewsetbook/<int:pk>/", views.BookInfoGenericApiViewSet.as_view({'get': 'retrieve'})),
    path("genericviewsetbook/<int:pk>/", views.BookInfoGenericApiViewSet.as_view({'get': 'retrieve'})),
    # path("img/cover/<int:pk>",views),
    path("genericviewgoodsintentory/", views.GoodsIntentoryListGenericApiViewSet.as_view({'get': 'list'})),
    path("genericviewgoodslist/", views.GoodsListGenericApiViewSet.as_view({'get': 'list'})),
    path("genericviewgoodslist/numslist/", views.GoodsListNumsListGenericApi.as_view()),
    path("genericviewboundjournallist/",
         views.BoundJournalListGenericApiViewSet.as_view({'get': 'list', 'post': "create"})),
    path("genericviewsqlstatment/",
         views.sqlStatementDocumentGenericApiViewSet.as_view({'get': 'list', 'post': 'create'})),
    path("genericviewsqlstatment/<int:pk>/",
         views.sqlStatementDocumentGenericApiViewSet.as_view({'get': 'retrieve', 'put': 'update'})),
    path("genericviewsqlstatment/test/",
         views.sqlStatementDocumentGenericApiViewSet.as_view({'get': 'test'})),
    # path("genericviewsqlstatment/<str:sysType>",
    #      views.sqlStatementDocumentGenericApiViewSet.as_view({'get': 'list', 'post': 'create', 'put': 'update'}))
]
# 创建路由
router = DefaultRouter()
# 注册路由
router.register('defaultrouterbook', views.BookInfoView)
# 把生成好的路由拼接到路由内
urlpatterns += router.urls
