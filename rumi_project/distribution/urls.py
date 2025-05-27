# distribution/urls.py
from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView
from .views import BookListView, BookCreateView, BookUpdateView, BookDeleteView
from .views import report_view, report_csv, report_pdf,home

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('books/', BookListView.as_view(), name='book_list'),
    # ... similar for book add/edit/delete ...
    path('report/', report_view, name='report'),
    path('report/csv/', report_csv, name='report_csv'),
    path('report/pdf/', report_pdf, name='report_pdf'),
    path('', home)
]
