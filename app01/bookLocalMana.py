import os, shutil
# import zipfile, zipp
# # import , py7zr, multivolumefile
# # from unrar import rarfile
import filetype
# from PIL import Image
# import configparser
import subprocess
# import itertools
# import time
#
# from PyQt5.QtGui import QStandardItemModel, QStandardItem
#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject5.settings")
# import django
#
# django.setup()
# from app01.models import Book
#
#
# class bookManager:
#     conf = configparser.ConfigParser()
#     conf.read(".\\TEST.ini", encoding='utf-8')
#     bookPath = conf.defaults()['bookzipspath']
#     booksPathDic = {}
#
#     def scanDirbooks(self):
#         DBtitleList = Book.objects.all().values_list('title', flat=True)
#         for root, dirs, files in os.walk(self.bookPath):
#             for file in files:
#                 filename = os.path.splitext(file)[0]
#                 exname = os.path.splitext(file)[1]
#                 if exname == ".zip":
#                     # 按照文件名称来判断是否一再数据库里
#                     if filename in DBtitleList:
#                         obj = Book.objects.get(title=filename)
#                         if (obj.path != root):
#                             obj.path = root
#                             obj.save()
#                     self.booksPathDic[filename] = root
#         print(self.booksPathDic)
#
#     # def addtoDB(self):
#     #     newBookslist = []
#     #     perviousBooks = Book.objects.all().order_by('-id')  # 为了取最后一条记录的id
#     #     # print(perviousBooks)
#     #     lastId = perviousBooks[0].id
#     #     for filename in self.resultList:
#     #         # newbook = Book.objects.create(title=filename)
#     #         # newbook.save()
#     #         newBookslist.append(Book(title=filename))
#     #         lastId += 1
#     #         self.generateCover(filename=filename, lastId=lastId)
#     #     Book.objects.bulk_create(newBookslist)
#
#     def addtoDB(self):
#         newBookslist = []
#         # perviousBooks = Book.objects.all().order_by('-id')  # 为了取最后一条记录的id
#         # print(perviousBooks)
#         # lastId = perviousBooks[0].id
#         for filename in self.booksPathDic.keys():
#             # newbook = Book.objects.create(title=filename)
#             # newbook.save()
#             newBookslist.append(Book(title=filename, path=self.booksPathDic[filename]))
#             # lastId += 1
#             # self.generateCover(filename=filename, lastId=lastId)
#         bulkCreateResponse = Book.objects.bulk_create(newBookslist)
#         for book in bulkCreateResponse:
#             self.generateCover(book.title, book.id)
#         pass
#
#     def generateCover(self, filename, lastId):
#         thumbnailSize = (400, 600)
#         if os.path.exists(f'''{self.booksPathDic[filename]}\\{filename}.zip'''):
#             # bookZip = zipfile.ZipFile(f'''{self.bookPath}\\{filename}.zip''', mode="r")
#             with zipfile.ZipFile(f'''{self.booksPathDic[filename]}\\{filename}.zip''', mode="r") as bookZip:
#                 # coverFile = bookZip.open(bookZip.filelist[0])
#                 for name in bookZip.namelist():
#                     # print(zipfile.Path(root=bookZip, at=name).is_dir())
#                     # coverFile = bookZip.open(name)
#                     if (zipp.Path(root=bookZip, at=name).is_file()):
#                         # print(zipfile.Path(root=bookZip, at=name).is_file())
#                         with bookZip.open(name) as coverFile:  # 这里似乎有bug
#                             # coverFile = bookZip.open(name)
#                             im = Image.open(coverFile)
#                             im.thumbnail(size=thumbnailSize)
#                             im.convert('RGB').save(f'''{self.bookPath}\\covers\\{lastId}.webp''', format="WebP",
#                                                    qulity=90)
#                         break
#
#             # im.show()
#             # print(bookZip)
#         else:
#             print("no exists")
#
#     def jxlTest(self):
#         tempList = []
#         for file in os.listdir(self.bookPath):
#             filename = os.path.splitext(file)[0]
#             exname = os.path.splitext(file)[1]
#             if exname == ".zip":
#                 tempList.append(filename)
#                 with zipfile.ZipFile(f'''{self.bookPath}\\{filename}.zip''', mode="r") as bookZip:
#                     # for name in bookZip.namelist():
#                     #     if (zipp.Path(root=bookZip, at=name).is_file()):
#                     #         with bookZip.open(name) as picFile:
#                     #             im = Image.open(picFile).show()
#                     os.mkdir(path=f'''{self.bookPath}\\{filename}\\''')
#                     bookZip.extractall(path=f'''{self.bookPath}\\{filename}\\''')
#                     print(f'''{filename}已解压''')
#                 for root, dirs, files in os.walk(f'''{self.bookPath}\\{filename}\\'''):
#                     for file in files:
#                         subprocess.run(
#                             f'''..\\utils\\cjxl.exe "{root}\\{file}" "{root}\\{os.path.splitext(file)[0]}.jxl"''',
#                             shell=True, stdout=subprocess.PIPE)
#                         os.remove(f'''{root}\\{file}''')
#                 with zipfile.ZipFile(f'''{self.bookPath}\\{filename}[jxl].zip''', mode='w') as newZip:
#                     for root2, dir2, files2 in os.walk(f'''{self.bookPath}\\{filename}\\'''):
#                         for file2 in files2:
#                             newZip.write(filename=f'''{root2}\\{file2}''', arcname=f'''{filename}\\{file2}''')
#                 shutil.rmtree(f'''{self.bookPath}\\{filename}''')
#
#     def rarExtractTest(self):
#         # rf = rarfile.RarFile('NO.106')
#         # for f in rf.infolist():
#         #     print(f.filename, f.file_size)
#         passwordList = ['123456', '1234567890', '12321312', '123456789', '1231241']
#         for root, dirs, files in os.walk('.\\archives0\\'):
#             for file in files:
#                 kind = filetype.guess(f'''{root}\\{file}''')
#                 fileTuple = os.path.splitext(f'''{root}\\{file}''')
#                 try:
#                     ext = kind.extension
#                     print(f'''{root}\\{file}''', "step1", ext)
#                 except Exception as e:
#                     print(f'''{root}\\{file}''', 'step2', e)
#                     continue
#                 for password in passwordList:
#                     try:
#                         if (ext == '7z' and fileTuple[1] == '.001'):
#                             with multivolumefile.open(fileTuple[0], mode='rb') as target_archive:
#                                 with py7zr.SevenZipFile(target_archive, mode='r', password=password) as archieve:
#                                     archieve.extractall(path=f'''{root}'''.replace('archives0', 'archives1'))
#                                     print('解压完成')
#                                     break
#                         if (ext == '7z'):
#                             archieve = py7zr.SevenZipFile(f'''{root}\\{file}''', mode='r', password=password)  # 密码在这里写
#                             archieve.extractall(path=f'''{root}'''.replace('archives0', 'archives1'))
#                             archieve.close()
#                             print('解压完成')
#                             break
#                         if (ext == 'rar'):
#                             archieve = rarfile.RarFile(f'''{root}\\{file}''', mode='r', )
#                             archieve.extractall(path=f'''{root}'''.replace('archives0', 'archives1'), pwd=password)
#                             print('解压完成')
#                             break
#                         if (ext == 'zip'):
#                             archieve = zipfile.ZipFile(f'''{root}\\{file}''', mode='r')
#                             archieve.extractall(path=f'''{root}'''.replace('archives0', 'archives1'),
#                                                 pwd=password.encode('utf-8'))
#                             print('解压完成')
#                             break
#                     except Exception as e:
#                         print(f'''{root}\\{file}''', 'step2', e)
#                         continue
#
#         for root, dirs, files in os.walk('.\\archives1\\'):
#             for file in files:
#                 kind = filetype.guess(f'''{root}\\{file}''')
#                 fileTuple = os.path.splitext(f'''{root}\\{file}''')
#                 try:
#                     ext = kind.extension  # 能被filetype识别到的文件类型
#                     print(f'''{root}\\{file}''', ext)
#                 except Exception as e:
#                     print(f'''{root}\\{file}''', 'step2', e)
#                     continue
#                 for password in passwordList:
#                     try:
#                         if (ext == '7z' and fileTuple[1] == '.001'):
#                             with multivolumefile.open(fileTuple[0], mode='rb') as target_archive:
#                                 with py7zr.SevenZipFile(target_archive, mode='r', password=password) as archieve:
#                                     archieve.extractall(path=f'''{root}'''.replace('archives1', 'archives2'))
#                                     print('解压完成')
#                                     break
#                         if (ext == '7z'):
#                             archieve = py7zr.SevenZipFile(f'''{root}\\{file}''', mode='r', password=password)
#                             archieve.extractall(path=f'''{root}'''.replace('archives1', 'archives2'))
#                             print('解压完成')
#                             break
#                         if (ext == 'rar'):
#                             archieve = rarfile.RarFile(f'''{root}\\{file}''', mode='r', )
#                             archieve.extractall(path=f'''{root}'''.replace('archives1', 'archives2'), pwd=password)
#                             print('解压完成')
#                             break
#                         if (ext == 'zip'):
#                             archieve = zipfile.ZipFile(f'''{root}\\{file}''', mode='r')
#                             archieve.extractall(path=f'''{root}'''.replace('archives1', 'archives2'),
#                                                 pwd=password.encode('utf-8'))
#                             print('解压完成')
#                             break
#                     except Exception as e:
#                         print(f'''{root}\\{file}''', 'step2', e)
#                         continue
#
#         for root, dirs, files in os.walk('.\\archives2\\'):
#             for file in files:
#                 ext = os.path.splitext(file)
#                 delTypeList = ('.txt', '.url')
#                 if (ext[-1] in delTypeList):
#                     os.remove(f'''{root}\\{file}''')
#                     print(f'''{root}\\{file}已删除''')
#         # kind = filetype.guess('.\\NO.106')
#         # print(kind.mime, kind.extension)
#
#         # shutil.register_archive_format('7zip', py7zr.pack_7zarchive, description='7zip archive')
#         # shutil.register_unpack_format('7zip', ['.7z'], py7zr.unpack_7zarchive, description='7zip archive')
#         # shutil.unpack_archive('.\\NO.106', '.\\temp')
#
#         # archive = py7zr.SevenZipFile('.\\temp\\NO.106', mode='r', password='hj8.top')
#         # archive.extractall(path=".\\temp")
#         # archive.close()
#
#     def convertJpgToJxl(self):
#         picList = []
#         for root, dirs, files in os.walk(
#                 r'C:\Users\lyy\workwork\djangoProject5\app01\static\jxl\真·中华小当家 Vol.12'):
#             for file in files:
#                 kind = filetype.guess(f'''{root}\\{file}''')
#                 if (kind == None):
#                     continue
#                 try:
#                     ext = kind.extension  # 能被filetype识别到的文件类型
#                     if (ext == 'jpg'):
#                         # subprocess.run(
#                         #     f'''..\\utils\\cjxl.exe "{root}\\{file}" "{root}\\{os.path.splitext(file)[0]}.jxl"''',
#                         #     shell=True, stdout=subprocess.PIPE)
#                         # subprocess.run(
#                         #     ['..\\utils\\cjxl.exe', f"{root}\\{file}", f"{root}\\{os.path.splitext(file)[0]}.jxl",
#                         #      "--lossless_jpeg=1"])
#                         picList.append(f'{root}\\{file}')
#                     if (ext == 'png'):
#                         # subprocess.run(
#                         #     ['..\\utils\\cjxl.exe', f"{root}\\{file}", f"{root}\\{os.path.splitext(file)[0]}.jxl",
#                         #      "--lossless_jpeg=0", '--quality=90'])
#                         picList.append(f'{root}\\{file}')
#                         # os.remove(f'''{root}\\{file}''')
#                 except Exception as ex:
#                     print(ex)
#
#         self.multiNum = 4
#         task_list = []
#         for index in range(len(picList) // self.multiNum + 1):
#             print(f'======================{index + 1}/{len(picList) // self.multiNum + 1}============================')
#             for path2 in picList[index * self.multiNum:index * self.multiNum + self.multiNum]:
#                 toJxl_task = subprocess.Popen(['..\\utils\\cjxl.exe', f"{path2}", f"{path2}.jxl",
#                                                "--lossless_jpeg=0", '--quality=90'])
#                 task_list.append(toJxl_task)
#             for task, index in zip(task_list, range(len(task_list))):
#                 while task.poll() is None:
#                     print(f'task{index} is running')
#                     time.sleep(0.5)
#                 print(f'task{index} is finished')
#             task_list.clear()
#

# #
# bm = bookManager()
# # bm.scanDirbooks()
# # bm.addtoDB()
# # bm.generateCover("真·中华小当家 Vol.01",1)
# # bm.jxlTest()
# # bm.rarExtractTest()
# bm.convertJpgToJxl()

import sys
from PyQt5.QtCore import QTimer, pyqtSignal, QObject, QThread
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QLineEdit, \
    QTextBrowser, QProgressBar, QTextEdit


class path_textBrower(QTextBrowser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAcceptDrops(True)
        self.urls_string_files = []
        self.urls_string_dirs = []

    def dragEnterEvent(self, e):

        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dragMoveEvent(self, e):
        pass

    def dropEvent(self, e):
        urls = [path for path in e.mimeData().urls()]
        achieve_exname = ('zip', 'rar', '7z')
        urls_string_files = []
        urls_string_dirs = []
        for url in urls:
            if os.path.isdir(url.path()[1:]):  # [1:]去除路径前的/字符
                urls_string_dirs.append(url.path()[1:])
            else:
                file_kind = filetype.guess(url.path()[1:])
                if file_kind is not None and file_kind.extension in achieve_exname:
                    urls_string_files.append(url.path()[1:])

        # 深度遍历下
        for url in urls_string_dirs:
            if os.path.isdir(url):
                for root, dirs, files in os.walk(url):
                    for file in files:
                        file_kind = filetype.guess(os.path.join(root, file))
                        if file_kind is not None and file_kind.extension in achieve_exname:
                            urls_string_files.append(os.path.join(root, file))

        if urls_string_files == []:
            self.setText('没有发现压缩文件')
        else:
            self.setText('\n'.join(urls_string_files))
            self.urls_string_files = urls_string_files


class Demo(QWidget):  # 1
    def __init__(self, multiNum):
        super(Demo, self).__init__()
        self.thread_1 = None

        self.button1 = QPushButton('开始', self)
        self.button1.clicked.connect(self.run_py)
        self.button2 = QPushButton('解压', self)
        self.button2.clicked.connect(self.extract_py)
        self.input_textBrower_logs = path_textBrower(self)
        self.output1_textBrower_logs = QTextBrowser(self)
        self.output2_textBrower_logs = QTextBrowser(self)
        self.password_texteditor_logs = QTextEdit(self)
        self.password_texteditor_logs.textChanged.connect(self.passwordListChanged)
        self.progressBar_all = QProgressBar(self)

        self.urls_string_files = []
        self.urls_string_dirs = []

        # self.bm = bookManager()
        # self.pathList = [r'C:\Users\lyy\workwork\djangoProject5\app01\static\jxl\真·中华小当家 Vol.12']
        # self.fileCount = 0
        # self.picDict = self.scanPics()
        self.multiNum = multiNum

        # for list in self.picDict.values():
        #     self.fileCount += len(list)

        # self.input_textBrower_logs.setText('\n'.join(self.picList))
        # self.progressBar_all.setRange(0, self.fileCount // self.multiNum)
        # self.progressBar_all.setValue(0)
        self.passwordList = ['123456', '123456789', '1234567890', '12321312', '1231241']
        self.password_texteditor_logs.setText('\n'.join(self.passwordList))
        self.password_texteditor_logs.textChanged.connect(self.updatePasswordList)
        self.layout_init()
        self.resize(700, 700)

    def passwordListChanged(self):
        self.passwordList = list(filter(bool, self.password_texteditor_logs.toPlainText().split('\n')))
        print("passwordListChanged", self.passwordList)

    def updatePasswordList(self):
        self.passwordList = self.password_texteditor_logs.toPlainText().split('\n')
        print()

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
        self.v_layout.addWidget(self.input_textBrower_logs)
        self.v_layout.addWidget(self.output1_textBrower_logs)

        self.h_layout4 = QHBoxLayout()
        self.h_layout4.addWidget(self.password_texteditor_logs)
        self.h_layout4.addWidget(self.output2_textBrower_logs)
        self.h_layout4.setStretch(1, 3)

        self.v_layout.addLayout(self.h_layout4)
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

    def extract_py(self):
        self.progressBar_all.setRange(0, len(self.input_textBrower_logs.urls_string_files))
        self.progressBar_all.setValue(0)
        self.thread_1 = bandizip_extract_thread(self.input_textBrower_logs.urls_string_files)
        self.thread_1.progressBarValue.connect(self.callback)
        self.thread_1.output1_set.connect(self.setOutput1Text)
        self.thread_1.output1_append.connect(self.appendOutput1Text)
        self.thread_1.output2_append.connect(self.appendOutput2Text)
        self.thread_1.start()

    def appendOutput1Text(self, index):
        textList1 = self.input_textBrower_logs.urls_string_files[:index]
        textList2 = self.input_textBrower_logs.urls_string_files[index:]
        self.output1_textBrower_logs.setText('\n'.join(textList1))
        self.input_textBrower_logs.setText('\n'.join(textList2))

    def appendOutput2Text(self, text):
        self.output2_textBrower_logs.append(text)

    def setOutput1Text(self, text):
        self.output1_textBrower_logs.setText(text)

    def setOutput2Text(self, text):
        self.output2_textBrower_logs.setText(text)


class bandizip_extract_thread(QThread):
    progressBarValue = pyqtSignal(int)  # 更新进度条
    signal_done = pyqtSignal(int)  # 是否结束信号

    output1_set = pyqtSignal(str)
    output2_append = pyqtSignal(str)
    output1_append = pyqtSignal(str)

    def __init__(self, urls_string_files):
        super(bandizip_extract_thread, self).__init__()
        self.passwordList = ['123456', '123456789', '1234567890', '12321312', '1231241']
        self.urls_string_files = urls_string_files

    def run(self):
        archives1 = []
        archives1DirsSet = set()
        for file_path, index in zip(self.urls_string_files, range(1, len(self.urls_string_files) + 1)):
            self.bandizip_extract(file_path, 'archives1')
            self.progressBarValue.emit(index)
            # new_file_path = os.path.join(os.path.dirname(file_path), 'archives1', os.path.basename(file_path))
            # self.output1_append.emit(new_file_path)
            archives1DirsSet.add(os.path.join(os.path.dirname(file_path), 'archives1'))
        # 工序2
        #  遍历所有archieves1文件夹
        for extractDir in archives1DirsSet:
            for root, dirs, files in os.walk(extractDir):
                for file in files:
                    file_kind = filetype.guess(os.path.join(root, file))
                    if file_kind is not None and file_kind.extension in ('rar', 'zip', '7z'):
                        archives1.append(os.path.join(root, file))
        self.output1_set.emit('\n'.join(archives1))
        self.progressBarValue.emit(0)
        #  再次开始解压
        for file, index2 in zip(archives1, range(1, len(archives1) + 1)):
            log = self.bandizip_extract(file, 'archives2')
            self.output2_append.emit(log)
            self.progressBarValue.emit(index2)
        self.output2_append.emit('结束哩')

    # for file_path, index in zip(self.urls_string_files, range(1, len(self.urls_string_files) + 1)):
    #     self.bandizip_extract(file_path)
    #     self.progressBarValue.emit(index)
    #     self.output1_append.emit(index)

    def bandizip_extract(self, file_path, archivesName):
        if not os.path.exists(os.path.join(os.path.dirname(file_path), archivesName)):
            os.mkdir(os.path.join(os.path.dirname(file_path), archivesName))
        for password in self.passwordList:
            try:
                task = subprocess.run(
                    [r'C:\Program Files\Bandizip\bz.exe', 'x', '-aoa', file_path,
                     os.path.join(os.path.dirname(file_path), archivesName)], shell=True, input=password.encode('gbk'),
                    check=True, capture_output=True
                )  # 解压覆盖模式
                # output = task.stdout.decode('gbk')[92:].split('\r\n')
                return task.stdout.decode('utf-8')
                break
            except subprocess.CalledProcessError as err:
                print(err)
            # out, err = extract_task.communicate()
            # print(out.decode('gbk'))
            # extract_task.stdin.write(b'123456789')
            # out, err = extract_task.communicate(input=password.encode('gbk'))
            # print(out.decode('gbk'))
            # print(err.decode('gbk'))


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
