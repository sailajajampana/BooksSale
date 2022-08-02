from django.contrib import admin

from books_app.api.models import Genre,Book

# Register your models here.
admin.site.register(Book)
admin.site.register(Genre)