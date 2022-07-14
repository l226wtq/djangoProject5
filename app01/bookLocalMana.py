import os, shutil
import zipfile, zipp, py7zr, multivolumefile
from unrar import rarfile
import filetype
from PIL import Image
import configparser
import subprocess

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject5.settings")
import django

django.setup()
from app01.models import Book


class bookManager:
    conf = configparser.ConfigParser()
    conf.read(".\\TEST.ini")
    bookPath = conf.defaults()['bookzipspath']
    resultList = []
    booksPathDic = {}

    def scanDirbooks(self):
        DBtitleList = Book.objects.all().values_list('title', flat=True)
        # for title in DBtitleList:
        #     print(title)
        # for file in os.listdir(self.bookPath):
        for root, dirs, files in os.walk(self.bookPath):
            for file in files:
                filename = os.path.splitext(file)[0]
                exname = os.path.splitext(file)[1]
                if exname == ".zip":
                    if filename in DBtitleList:
                        continue  # 文件重复了
                    self.resultList.append(filename)
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
        for root, dirs, files in os.walk('.\\tojxl\\'):
            for file in files:
                kind = filetype.guess(f'''{root}\\{file}''')
                print(kind)
                try:
                    ext = kind.extension  # 能被filetype识别到的文件类型
                    if (ext == 'jpg'):
                        subprocess.run(
                            f'''..\\utils\\cjxl.exe "{root}\\{file}" "{root}\\{os.path.splitext(file)[0]}.jxl"''',
                            shell=True, stdout=subprocess.PIPE)
                        os.remove(f'''{root}\\{file}''')
                except Exception as ex:
                    print(ex)


bm = bookManager()
bm.scanDirbooks()
bm.addtoDB()
# bm.generateCover("真·中华小当家 Vol.01",1)
# bm.jxlTest()
# bm.rarExtractTest()
# bm.convertJpgToJxl()
