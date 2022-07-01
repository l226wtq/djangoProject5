import os
import zipfile, zipp
from PIL import Image

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoProject5.settings")
import django

django.setup()
from app01.models import Book


class bookManager:
    bookPath = "C:\\Users\\lyy\\PycharmProjects\\djangoProject5\\app01\\static\\bookZips"
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

    def addtoDB(self):
        newBookslist = []
        perviousBooks = Book.objects.all().order_by('-id')  # 为了取最后一条记录的id
        # print(perviousBooks)
        lastId = perviousBooks[0].id
        for filename in self.resultList:
            # newbook = Book.objects.create(title=filename)
            # newbook.save()
            newBookslist.append(Book(title=filename))
            lastId += 1
            self.generateCover(filename=filename, lastId=lastId)
        Book.objects.bulk_create(newBookslist)

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
                            im.save(f'''{self.bookPath}\\covers\\{lastId}.jpg''', qulity=90)
                        break

            # im.show()
            # print(bookZip)
        else:
            print("no exists")


bm = bookManager()
bm.scanDirbooks()
bm.addtoDB()
# bm.generateCover("真·中华小当家 Vol.01",1)
