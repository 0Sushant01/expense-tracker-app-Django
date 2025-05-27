# distribution/views.py
import pandas as pd
import camelot
import csv
import tempfile
from io import BytesIO
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Sum
from .models import Book, Category
from .forms import UploadFileForm
from django.views.generic import TemplateView
from django.http import JsonResponse

def import_data(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            try:
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)

                elif file.name.endswith('.pdf'):
                    # Save uploaded file to a temp file so Camelot can read it
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
                        for chunk in file.chunks():
                            temp_pdf.write(chunk)
                        temp_pdf_path = temp_pdf.name

                    tables = camelot.read_pdf(temp_pdf_path, pages='all')
                    if tables and len(tables) > 0:
                        df = tables[0].df
                        df.columns = df.iloc[0]  # Set header
                        df = df.drop(index=0)
                    else:
                        messages.error(request, "No tables found in PDF.")
                        return redirect('import_data')
                else:
                    messages.error(request, "Unsupported file format. Upload .csv or .pdf.")
                    return redirect('import_data')

                # Save data to DB
                for _, row in df.iterrows():
                    cat, _ = Category.objects.get_or_create(name=row['Category'])
                    Book.objects.get_or_create(
                        title=row['Title'],
                        author=row['Author'],
                        publication_date=row['Date'],
                        category=cat,
                        distribution_expenses=row['Expense']
                    )

                messages.success(request, "Data imported successfully!")
                return redirect('book_list')

            except Exception as e:
                messages.error(request, f"Error processing file: {e}")
                return redirect('import_data')
    else:
        form = UploadFileForm()

    return render(request, 'import.html', {'form': form})


def report_view(request):
    data = Book.objects.values('category__name').annotate(total=Sum('distribution_expenses'))
    return render(request, 'report.html', {'report': data})


def report_csv(request):
    data = Book.objects.values('category__name').annotate(total=Sum('distribution_expenses'))
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses_by_category.csv"'
    writer = csv.writer(response)
    writer.writerow(['Category', 'Total Expenses'])
    for row in data:
        writer.writerow([row['category__name'], row['total']])
    return response


def report_pdf(request):
    data = Book.objects.values('category__name').annotate(total=Sum('distribution_expenses'))
    template = get_template('report.html')
    html = template.render({'report': data})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expenses_by_category.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response

# Add to distribution/views.py

from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

# Category Views
class CategoryListView(ListView):
    model = Category
    template_name = 'category_list.html'

class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    template_name = 'category_form.html'
    success_url = reverse_lazy('category_list')

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'category_confirm_delete.html'
    success_url = reverse_lazy('category_list')


# Book Views
class BookListView(ListView):
    model = Book
    template_name = 'book_list.html'

class BookCreateView(CreateView):
    model = Book
    fields = ['title', 'author', 'publication_date', 'category', 'distribution_expenses']
    template_name = 'book_form.html'
    success_url = reverse_lazy('book_list')

class BookUpdateView(UpdateView):
    model = Book
    fields = ['title', 'author', 'publication_date', 'category', 'distribution_expenses']
    template_name = 'book_form.html'
    success_url = reverse_lazy('book_list')

class BookDeleteView(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

class HomePageView(TemplateView):
    template_name = 'home.html'


def home_chart_data(request):
    data = Book.objects.values('category__name').annotate(total=Sum('distribution_expenses'))
    chart_data = {
        'labels': [item['category__name'] for item in data],
        'data': [float(item['total']) for item in data]
    }
    return JsonResponse(chart_data)
