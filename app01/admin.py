from django.contrib import admin
from .models import Book, BoundJournalList,sqlStatementDocument,sqlSingleStatmentList

# Register your models here.
admin.site.register(Book)
admin.site.register(BoundJournalList)
admin.site.register(sqlStatementDocument)
admin.site.register(sqlSingleStatmentList)
