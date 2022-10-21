import os, shutil
import zipfile, zipp
# import , py7zr, multivolumefile
# from unrar import rarfile
import filetype
from PIL import Image
import configparser
import subprocess
import itertools
import time

from PyQt5.QtGui import QStandardItemModel, QStandardItem

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject5.settings")
import django

django.setup()
from app01.models import Book


class bookManager:
    conf = configparser.ConfigParser()
    conf.read(".\\TEST.ini")
    bookPath = conf.defaults()['bookzipspath']
    booksPathDic = {}

    def scanDirbooks(self):
        DBtitleList = Book.objects.all().values_list('title', flat=True)
        for root, dirs, files in os.walk(self.bookPath):
            for file in files:
                filename = os.path.splitext(file)[0]
                exname = os.path.splitext(file)[1]
                if exname == ".zip":
                    # 按照文件名称来判断是否一再数据库里
                    if filename in DBtitleList:
                        obj = Book.objects.get(title=filename)
                        if (obj.path != root):
                            obj.path = root
                            obj.save()
                    self.booksPathDic[filename] = root
        print(self.booksPathDic)

    # def addtoDB(self):
    #     newBookslist = []
    #     perviousBooks = Book.objects.all().order_by('-id')  # 为了取最后一条记录的id
    #     # print(perviousBooks)
    #     lastId = perviousBooks[0].id
    #     for filename in self.resultList:
    #         # newbook = Book.objects.create(title=filename)
    #         # newbook.save()
    #         newBookslist.append(Book(title=filename))
    #         lastId += 1
    #         self.generateCover(filename=filename, lastId=lastId)
    #     Book.objects.bulk_create(newBookslist)

    def addtoDB(self):
        newBookslist = []
        # perviousBooks = Book.objects.all().order_by('-id')  # 为了取最后一条记录的id
        # print(perviousBooks)
        # lastId = perviousBooks[0].id
        for filename in self.booksPathDic.keys():
            # newbook = Book.objects.create(title=filename)
            # newbook.save()
            newBookslist.append(Book(title=filename, path=self.booksPathDic[filename]))
            # lastId += 1
            # self.generateCover(filename=filename, lastId=lastId)
        bulkCreateResponse = Book.objects.bulk_create(newBookslist)
        for book in bulkCreateResponse:
            self.generateCover(book.title, book.id)
        pass

    def generateCover(self, filename, lastId):
        thumbnailSize = (400, 600)
        if os.path.exists(f'''{self.booksPathDic[filename]}\\{filename}.zip'''):
            # bookZip = zipfile.ZipFile(f'''{self.bookPath}\\{filename}.zip''', mode="r")
            with zipfile.ZipFile(f'''{self.booksPathDic[filename]}\\{filename}.zip''', mode="r") as bookZip:
                # coverFile = bookZip.open(bookZip.filelist[0])
                for name in bookZip.namelist():
                    # print(zipfile.Path(root=bookZip, at=name).is_dir())
                    # coverFile = bookZip.open(name)
                    if (zipp.Path(root=bookZip, at=name).is_file()):
                        # print(zipfile.Path(root=bookZip, at=name).is_file())
                        with bookZip.open(name) as coverFile:  # 这里似乎有bug
                            # coverFile = bookZip.open(name)
                            im = Image.open(coverFile)
                            im.thumbnail(size=thumbnailSize)
                            im.convert('RGB').save(f'''{self.bookPath}\\covers\\{lastId}.webp''', format="WebP",
                                                   qulity=90)
                        break

            # im.show()
            # print(bookZip)
        else:
            print("no exists")

    def jxlTest(self):
        tempList = []
        for file in os.listdir(self.bookPath):
            filename = os.path.splitext(file)[0]
            exname = os.path.splitext(file)[1]
            if exname == ".zip":
                tempList.append(filename)
                with zipfile.ZipFile(f'''{self.bookPath}\\{filename}.zip''', mode="r") as bookZip:
                    # for name in bookZip.namelist():
                    #     if (zipp.Path(root=bookZip, at=name).is_file()):
                    #         with bookZip.open(name) as picFile:
                    #             im = Image.open(picFile).show()
                    os.mkdir(path=f'''{self.bookPath}\\{filename}\\''')
                    bookZip.extractall(path=f'''{self.bookPath}\\{filename}\\''')
                    print(f'''{filename}已解压''')
                for root, dirs, files in os.walk(f'''{self.bookPath}\\{filename}\\'''):
                    for file in files:
                        subprocess.run(
                            f'''..\\utils\\cjxl.exe "{root}\\{file}" "{root}\\{os.path.splitext(file)[0]}.jxl"''',
                            shell=True, stdout=subprocess.PIPE)
                        os.remove(f'''{root}\\{file}''')
                with zipfile.ZipFile(f'''{self.bookPath}\\{filename}[jxl].zip''', mode='w') as newZip:
                    for root2, dir2, files2 in os.walk(f'''{self.bookPath}\\{filename}\\'''):
                        for file2 in files2:
                            newZip.write(filename=f'''{root2}\\{file2}''', arcname=f'''{filename}\\{file2}''')
                shutil.rmtree(f'''{self.bookPath}\\{filename}''')

    def rarExtractTest(self):
        # rf = rarfile.RarFile('NO.106')
        # for f in rf.infolist():
        #     print(f.filename, f.file_size)
        passwordList = ['123456', '1234567890', '12321312', '123456789', '1231241']
        for root, dirs, files in os.walk('.\\archives0\\'):
            for file in files:
                kind = filetype.guess(f'''{root}\\{file}''')
                fileTuple = os.path.splitext(f'''{root}\\{file}''')
                try:
                    ext = kind.extension
                    print(f'''{root}\\{file}''', "step1", ext)
                except Exception as e:
                    print(f'''{root}\\{file}''', 'step2', e)
                    continue
                for password in passwordList:
                    try:
                        if (ext == '7z' and fileTuple[1] == '.001'):
                            with multivolumefile.open(fileTuple[0], mode='rb') as target_archive:
                                with py7zr.SevenZipFile(target_archive, mode='r', password=password) as archieve:
                                    archieve.extractall(path=f'''{root}'''.replace('archives0', 'archives1'))
                                    print('解压完成')
                                    break
                        if (ext == '7z'):
                            archieve = py7zr.SevenZipFile(f'''{root}\\{file}''', mode='r', password=password)  # 密码在这里写
                            archieve.extractall(path=f'''{root}'''.replace('archives0', 'archives1'))
                            archieve.close()
                            print('解压完成')
                            break
                        if (ext == 'rar'):
                            archieve = rarfile.RarFile(f'''{root}\\{file}''', mode='r', )
                            archieve.extractall(path=f'''{root}'''.replace('archives0', 'archives1'), pwd=password)
                            print('解压完成')
                            break
                        if (ext == 'zip'):
                            archieve = zipfile.ZipFile(f'''{root}\\{file}''', mode='r')
                            archieve.extractall(path=f'''{root}'''.replace('archives0', 'archives1'),
                                                pwd=password.encode('utf-8'))
                            print('解压完成')
                            break
                    except Exception as e:
                        print(f'''{root}\\{file}''', 'step2', e)
                        continue

        for root, dirs, files in os.walk('.\\archives1\\'):
            for file in files:
                kind = filetype.guess(f'''{root}\\{file}''')
                fileTuple = os.path.splitext(f'''{root}\\{file}''')
                try:
                    ext = kind.extension  # 能被filetype识别到的文件类型
                    print(f'''{root}\\{file}''', ext)
                except Exception as e:
                    print(f'''{root}\\{file}''', 'step2', e)
                    continue
                for password in passwordList:
                    try:
                        if (ext == '7z' and fileTuple[1] == '.001'):
                            with multivolumefile.open(fileTuple[0], mode='rb') as target_archive:
                                with py7zr.SevenZipFile(target_archive, mode='r', password=password) as archieve:
                                    archieve.extractall(path=f'''{root}'''.replace('archives1', 'archives2'))
                                    print('解压完成')
                                    break
                        if (ext == '7z'):
                            archieve = py7zr.SevenZipFile(f'''{root}\\{file}''', mode='r', password=password)
                            archieve.extractall(path=f'''{root}'''.replace('archives1', 'archives2'))
                            print('解压完成')
                            break
                        if (ext == 'rar'):
                            archieve = rarfile.RarFile(f'''{root}\\{file}''', mode='r', )
                            archieve.extractall(path=f'''{root}'''.replace('archives1', 'archives2'), pwd=password)
                            print('解压完成')
                            break
                        if (ext == 'zip'):
                            archieve = zipfile.ZipFile(f'''{root}\\{file}''', mode='r')
                            archieve.extractall(path=f'''{root}'''.replace('archives1', 'archives2'),
                                                pwd=password.encode('utf-8'))
                            print('解压完成')
                            break
                    except Exception as e:
                        print(f'''{root}\\{file}''', 'step2', e)
                        continue

        for root, dirs, files in os.walk('.\\archives2\\'):
            for file in files:
                ext = os.path.splitext(file)
                delTypeList = ('.txt', '.url')
                if (ext[-1] in delTypeList):
                    os.remove(f'''{root}\\{file}''')
                    print(f'''{root}\\{file}已删除''')
        # kind = filetype.guess('.\\NO.106')
        # print(kind.mime, kind.extension)

        # shutil.register_archive_format('7zip', py7zr.pack_7zarchive, description='7zip archive')
        # shutil.register_unpack_format('7zip', ['.7z'], py7zr.unpack_7zarchive, description='7zip archive')
        # shutil.unpack_archive('.\\NO.106', '.\\temp')

        # archive = py7zr.SevenZipFile('.\\temp\\NO.106', mode='r', password='hj8.top')
        # archive.extractall(path=".\\temp")
        # archive.close()

    def convertJpgToJxl(self):
        picList = []
        for root, dirs, files in os.walk(
                r'C:\Users\lyy\workwork\djangoProject5\app01\static\jxl\真·中华小当家 Vol.12'):
            for file in files:
                kind = filetype.guess(f'''{root}\\{file}''')
                if (kind == None):
                    continue
                try:
                    ext = kind.extension  # 能被filetype识别到的文件类型
                    if (ext == 'jpg'):
                        # subprocess.run(
                        #     f'''..\\utils\\cjxl.exe "{root}\\{file}" "{root}\\{os.path.splitext(file)[0]}.jxl"''',
                        #     shell=True, stdout=subprocess.PIPE)
                        # subprocess.run(
                        #     ['..\\utils\\cjxl.exe', f"{root}\\{file}", f"{root}\\{os.path.splitext(file)[0]}.jxl",
                        #      "--lossless_jpeg=1"])
                        picList.append(f'{root}\\{file}')
                    if (ext == 'png'):
                        # subprocess.run(
                        #     ['..\\utils\\cjxl.exe', f"{root}\\{file}", f"{root}\\{os.path.splitext(file)[0]}.jxl",
                        #      "--lossless_jpeg=0", '--quality=90'])
                        picList.append(f'{root}\\{file}')
                        # os.remove(f'''{root}\\{file}''')
                except Exception as ex:
                    print(ex)

        self.multiNum = 4
        task_list = []
        for index in range(len(picList) // self.multiNum + 1):
            print(f'======================{index + 1}/{len(picList) // self.multiNum + 1}============================')
            for path2 in picList[index * self.multiNum:index * self.multiNum + self.multiNum]:
                toJxl_task = subprocess.Popen(['..\\utils\\cjxl.exe', f"{path2}", f"{path2}.jxl",
                                               "--lossless_jpeg=0", '--quality=90'])
                task_list.append(toJxl_task)
            for task, index in zip(task_list, range(len(task_list))):
                while task.poll() is None:
                    print(f'task{index} is running')
                    time.sleep(0.5)
                print(f'task{index} is finished')
            task_list.clear()


# #
# bm = bookManager()
# # bm.scanDirbooks()
# # bm.addtoDB()
# # bm.generateCover("真·中华小当家 Vol.01",1)
# # bm.jxlTest()
# # bm.rarExtractTest()
# bm.convertJpgToJxl()

import sys
from threading import Thread
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QTextBrowser, QProgressBar


# 信号库
class SignalStore(QObject):
    # 定义一种信号
    progress_update = pyqtSignal(int)
    # 还可以定义其他作用的信号


# 实例化
so = SignalStore()


class Demo(QWidget):  # 1
    def __init__(self, multiNum):
        super(Demo, self).__init__()
        self.thread_1 = None

        self.button1 = QPushButton('开始', self)
        self.button1.clicked.connect(self.run_py)
        self.button2 = QPushButton('结束', self)
        self.textBrower_logs = QTextBrowser(self)
        self.setAcceptDrops(True)
        self.progressBar_all = QProgressBar(self)

        self.bm = bookManager()
        self.pathList = [r'C:\Users\lyy\workwork\djangoProject5\app01\static\jxl\真·中华小当家 Vol.12']
        self.fileCount = 0
        self.picDict = self.scanPics()
        self.multiNum = multiNum

        for list in self.picDict.values():
            self.fileCount += len(list)

        # self.textBrower_logs.setText('\n'.join(self.picList))
        self.progressBar_all.setRange(0, self.fileCount // self.multiNum)
        self.progressBar_all.setValue(0)

        self.layout_init()
        self.resize(700, 700)

    def dragEnterEvent(self, QDragEnterEvent):  # 3
        print('Drag Enter')

    def dragMoveEvent(self, QDragMoveEvent):  # 4
        print('Drag Move')

    def dragLeaveEvent(self, QDragLeaveEvent):  # 5
        print('Drag Leave')

    def dropEvent(self, QDropEvent):  # 6
        print('Drag Drop')

    def scanPics(self):
        tempDict = {'jpg': [], 'png': []}
        for rootPath in self.pathList:
            for root, dirs, files in os.walk(rootPath):
                for file in files:
                    kind = filetype.guess(f'''{root}\\{file}''')
                    if (kind == None):
                        continue
                    try:
                        ext = kind.extension  # 能被filetype识别到的文件类型
                        if (ext == 'jpg'):
                            tempDict['jpg'].append(f'{root}\\{file}')
                        if (ext == 'png'):
                            tempDict['png'].append(f'{root}\\{file}')
                    except Exception as ex:
                        print(ex)
        return tempDict

    def layout_init(self):
        self.h_layout3 = QHBoxLayout()
        self.h_layout3.addWidget(self.button1)
        self.h_layout3.addWidget(self.button2)

        self.v_layout = QVBoxLayout()
        self.v_layout.addLayout(self.h_layout3)
        self.v_layout.addWidget(self.textBrower_logs)
        self.v_layout.addWidget(self.progressBar_all)

        self.setLayout(self.v_layout)

    def run_py(self):
        self.progressBar_all.setValue(0)
        self.thread_1 = Runthread(picsDic=self.picDict, multiNum=self.multiNum)
        self.thread_1.progressBarValue.connect(self.callback)
        self.thread_1.start()

    # 回传进度条参数
    def callback(self, i):
        self.progressBar_all.setValue(i)


class Runthread(QThread):
    progressBarValue = pyqtSignal(int)  # 更新进度条
    signal_done = pyqtSignal(int)  # 是否结束信号

    def __init__(self, picsDic, multiNum):
        super(Runthread, self).__init__()
        self.picsDic = picsDic
        self.multiNum = multiNum
        self.jpgLen = len(self.picsDic['jpg'])
        self.pngLen = len(self.picsDic['png'])

    def run(self):
        task_list = []

        # 先处理jpg2jxl
        for index1 in range(self.jpgLen // self.multiNum + 1):
            print('jpg', index1, self.jpgLen // self.multiNum + 1)
            for path2 in self.picsDic['jpg'][index1 * self.multiNum:index1 * self.multiNum + self.multiNum]:
                toJxl_task = subprocess.Popen(['..\\utils\\cjxl.exe', f"{path2}", f"{path2}.jxl",
                                               "--lossless_jpeg=1"])
                task_list.append(toJxl_task)
            for task, index2 in zip(task_list, range(len(task_list))):
                while task.poll() is None:
                    print(f'task{index2} is running')
                    time.sleep(0.5)
                print(f'task{index2} is finished')
            task_list.clear()
            self.progressBarValue.emit(index1)  # 发送进度条的值信号

            # 再处理png2jxl
            for index1 in range(self.pngLen // self.multiNum + 1):
                print('png', index1, self.pngLen // self.multiNum + 1)
                for path2 in self.picsDic['jpg'][index1 * self.multiNum:index1 * self.multiNum + self.multiNum]:
                    toJxl_task = subprocess.Popen(['..\\utils\\cjxl.exe', f"{path2}", f"{path2}.jxl",
                                                   "--quality=90"])
                    task_list.append(toJxl_task)
                for task, index2 in zip(task_list, range(len(task_list))):
                    while task.poll() is None:
                        print(f'task{index2} is running')
                        time.sleep(0.5)
                    print(f'task{index2} is finished')
                task_list.clear()
            self.progressBarValue.emit(index1 + self.jpgLen)  # 发送进度条的值信号


if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = Demo(multiNum=4)

    demo.show()  # 7
    sys.exit(app.exec_())

# import sys
# from PyQt5.QtWidgets import QWidget, QApplication, QTreeView, QFileSystemModel, QHBoxLayout
# from PyQt5 import QtCore
# from PyQt5.Qt import *
#
#
# class MainWidget(QWidget):
#     def __init__(self, parent=None):
#         super(MainWidget, self).__init__(parent)
#
#         # 获取系统所有文件
#         self.model01 = QFileSystemModel()
#         # 进行筛选只显示文件夹，不显示文件和特色文件
#         self.model01.setFilter(QtCore.QDir.Dirs | QtCore.QDir.NoDotAndDotDot)
#         self.model01.setRootPath('')
#
#         # 定义创建左边窗口
#         self.treeView1 = QTreeView(self)
#         self.treeView1.setModel(self.model01)
#         for col in range(1, 4):
#             self.treeView1.setColumnHidden(col, True)
#         self.treeView1.doubleClicked.connect(self.initUI)
#
#         # 定义创建右边窗口
#         self.model02 = QStandardItemModel()
#         self.treeView2 = QTreeView(self)
#         self.treeView2.setModel(self.model02)
#
#         # 将创建的窗口进行添加
#         self.layout = QHBoxLayout()
#         self.layout.addWidget(self.treeView1)
#         self.layout.addWidget(self.treeView2)
#         self.setLayout(self.layout)
#
#     def initUI(self, Qmodelidx):
#         # 每次点击清空右边窗口数据
#         self.model02.clear()
#         # 定义一个数组存储路径下的所有文件
#         PathData = []
#         # 获取双击后的指定路径
#         filePath = self.model01.filePath(Qmodelidx)
#         # List窗口文件赋值
#         PathDataName = self.model02.invisibleRootItem()
#         # 拿到文件夹下的所有文件
#         PathDataSet = os.listdir(filePath)
#         # 进行将拿到的数据进行排序
#         PathDataSet.sort()
#         # 遍历判断拿到的文件是文件夹还是文件，Flase为文件，True为文件夹
#         for Data in range(len(PathDataSet)):
#             if os.path.isdir(filePath + '\\' + PathDataSet[Data]) == False:
#                 PathData.append(PathDataSet[Data])
#             elif os.path.isdir(filePath + '\\' + PathDataSet[Data]) == True:
#                 print('2')
#         # 将拿到的所有文件放到数组中进行右边窗口赋值。
#         for got in range(len(PathData)):
#             gosData = QStandardItem(PathData[got])
#             PathDataName.setChild(got, gosData)
#
# app = QApplication(sys.argv)
# widget = MainWidget()
# # widget.resize(640, 480)
# widget.setWindowTitle("Hello, PyQt5!")
# widget.show()
# sys.exit(app.exec())
# import sys
# # PyQt5中使用的基本控件都在PyQt5.QtWidgets模块中
# from PyQt5.QtWidgets import QApplication, QMainWindow
# # 导入designer工具生成的login模块
#
# from PyQt5 import QtCore, QtGui, QtWidgets
#
#
# class Ui_Dialog(object):
#     def setupUi(self, Dialog):
#         Dialog.setObjectName("Dialog")
#         Dialog.resize(800, 800)
#         self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
#         self.buttonBox.setGeometry(QtCore.QRect(420, 740, 341, 32))
#         self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
#         self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
#         self.buttonBox.setObjectName("buttonBox")
#         self.frame = QtWidgets.QFrame(Dialog)
#         self.frame.setGeometry(QtCore.QRect(60, 40, 521, 481))
#         self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
#         self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
#         self.frame.setObjectName("frame")
#         self.progressBar = QtWidgets.QProgressBar(self.frame)
#         self.progressBar.setGeometry(QtCore.QRect(50, 440, 421, 23))
#         self.progressBar.setProperty("value", 24)
#         self.progressBar.setObjectName("progressBar")
#         self.pushButton = QtWidgets.QPushButton(self.frame)
#         self.pushButton.setGeometry(QtCore.QRect(40, 190, 111, 41))
#         self.pushButton.setObjectName("pushButton")
#
#         self.retranslateUi(Dialog)
#         # self.buttonBox.accepted.connect(Dialog.accept)  # type: ignore
#         # self.buttonBox.rejected.connect(Dialog.reject)  # type: ignore
#         QtCore.QMetaObject.connectSlotsByName(Dialog)
#
#     def retranslateUi(self, Dialog):
#         _translate = QtCore.QCoreApplication.translate
#         Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
#         self.pushButton.setText(_translate("Dialog", "PushButton"))
#
#
# class MyMainForm(QMainWindow, Ui_Dialog):
#     def __init__(self, parent=None):
#         super(MyMainForm, self).__init__(parent)
#         self.setupUi(self)
#
#
# if __name__ == "__main__":
#     # 固定的，PyQt5程序都需要QApplication对象。sys.argv是命令行参数列表，确保程序可以双击运行
#     app = QApplication(sys.argv)
#     # 初始化
#     myWin = MyMainForm()
#     # 将窗口控件显示在屏幕上
#     myWin.show()
#     # 程序运行，sys.exit方法确保程序完整退出。
#     sys.exit(app.exec_())
