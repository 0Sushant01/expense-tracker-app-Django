from django.urls import path
from .views import (
    CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView,
    BookListView, BookCreateView, BookUpdateView, BookDeleteView,
    report_view, report_csv, report_pdf,
    import_data,
    HomePageView
)
from .views import home_chart_data

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/add/', CategoryCreateView.as_view(), name='category_add'),
    path('categories/<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('books/add/', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book_delete'),
    path('import/', import_data, name='import_data'),  # ✅ THIS FIXES YOUR ERROR
    path('report/', report_view, name='report'),
    path('report/csv/', report_csv, name='report_csv'),
    path('report/pdf/', report_pdf, name='report_pdf'),
    path('chart-data/', home_chart_data, name='home_chart_data'),
]
