from django.contrib import admin
from .models import Rental, Book, Film, CD


# Register your models here.

class BooksInLine(admin.TabularInline):
    model = Book
    extra = 0


class FilmInLine(admin.TabularInline):
    model = Film
    extra = 0


class CDInline(admin.TabularInline):
    model = CD
    extra = 0


class RentalAdmin(admin.ModelAdmin):
    inlines = [BooksInLine, FilmInLine, CDInline]
    list_display = ('name', 'get_address')
    list_filter = ['province']
    search_fields = ['name', 'city']


admin.site.register(Rental, RentalAdmin)
