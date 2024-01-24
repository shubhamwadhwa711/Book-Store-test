from django.contrib import admin
from .models import Author, Book, StoringInformation

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'birth_date')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_year', 'author', 'barcode', 'available_quantity')
    search_fields = ('title', 'author__name', 'barcode')
    list_filter = ('author', 'publish_year')

@admin.register(StoringInformation)
class StoringInformationAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity', 'action', 'created_at')
    search_fields = ('book__title',)
    list_filter = ('action', 'created_at')
