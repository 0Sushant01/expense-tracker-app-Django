from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Category, Book

class CategoryResource(resources.ModelResource):
    class Meta:
        model = Category

class BookResource(resources.ModelResource):
    class Meta:
        model = Book

@admin.register(Category)
class CategoryAdmin(ImportExportModelAdmin):
    resource_class = CategoryResource
    list_display = ('name',)

@admin.register(Book)
class BookAdmin(ImportExportModelAdmin):
    resource_class = BookResource
    list_display = ('title', 'author', 'category', 'publication_date', 'distribution_expenses')
    list_filter = ('category',)
    search_fields = ('title', 'author')
