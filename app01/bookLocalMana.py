import os, shutil
import zipfile, zipp
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

    def scanDirbooks(self):
        DBtitleList = Book.objects.all().values_list('title', flat=True)
        # for title in DBtitleList:
        #     print(title)
        for file in os.listdir(self.bookPath):

            filename = os.path.splitext(file)[0]
            exname = os.path.splitext(file)[1]
            if exname == ".zip":
                if filename in DBtitleList:
                    continue  # 文件重复了
                self.resultList.append(filename)
        print(self.resultList)

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
        for filename in self.resultList:
            # newbook = Book.objects.create(title=filename)
            # newbook.save()
            newBookslist.append(Book(title=filename))
            # lastId += 1
            # self.generateCover(filename=filename, lastId=lastId)
        bulkCreateResponse = Book.objects.bulk_create(newBookslist)
        for book in bulkCreateResponse:
            self.generateCover(book.title, book.id)
        pass

    def generateCover(self, filename, lastId):
        thumbnailSize = (400, 600)
        if os.path.exists(f'''{self.bookPath}\\{filename}.zip'''):
            # bookZip = zipfile.ZipFile(f'''{self.bookPath}\\{filename}.zip''', mode="r")
            with zipfile.ZipFile(f'''{self.bookPath}\\{filename}.zip''', mode="r") as bookZip:
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
        # if os.path.exists(f'''{self.bookPath}\\{filename}.zip'''):
        #     # bookZip = zipfile.ZipFile(f'''{self.bookPath}\\{filename}.zip''', mode="r")
        #     with zipfile.ZipFile(f'''{self.bookPath}\\{filename}.zip''', mode="r") as bookZip:
        #         # coverFile = bookZip.open(bookZip.filelist[0])
        #         for name in bookZip.namelist():
        #             # print(zipfile.Path(root=bookZip, at=name).is_dir())
        #             # coverFile = bookZip.open(name)
        #             if (zipp.Path(root=bookZip, at=name).is_file()):
        #                 # print(zipfile.Path(root=bookZip, at=name).is_file())
        #                 with bookZip.open(name) as coverFile:  # 这里似乎有bug
        #                     # coverFile = bookZip.open(name)
        #                     im = Image.open(coverFile)
        #                     im.thumbnail(size=thumbnailSize)
        #                     im.convert('RGB').save(f'''{self.bookPath}\\covers\\{lastId}.webp''', format="WebP",
        #                                            qulity=90)
        #                 break
        # print(subprocess.run('..\\utils\\cjxl.exe .\\static\\bookContent\\0001.jpg .\\static\\bookContent\\0001.jxl', shell=True, stdout=subprocess.PIPE).stdout.decode('gbk'))
        # subprocess.run('..\\utils\\cjxl.exe .\\static\\bookContent\\pic1.jpg .\\static\\bookContent\\pic1.jxl',
        #                shell=True, stdout=subprocess.PIPE)

        # print(subprocess.run('..\\utils\\cjxl.exe -h', shell=True, stdout=subprocess.PIPE).stdout.decode('gbk'))
        # p = subprocess.Popen('ping baidu.com',
        #                      stdin=subprocess.PIPE,
        #                      stdout=subprocess.PIPE,
        #                      stderr=subprocess.PIPE, shell=True)
        # out = p.stdout.read().decode('gbk')
        # print(out)


bm = bookManager()
# bm.scanDirbooks()
# bm.addtoDB()
# bm.generateCover("真·中华小当家 Vol.01",1)
bm.jxlTest()
