from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from movies.models import Movie
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from openpyxl import Workbook
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from io import BytesIO

# Create your views here.
User = get_user_model()
class DashboardView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'dashboard/dashboard.html'
    total_movies = Movie.objects.count()
    # total_users = User.objects.filter(role='user').count()

    def test_func(self):
        # Check if the user is a superuser
        return self.request.user.is_superuser

dashboard_view = DashboardView.as_view()

def create_movie(request):
    if request.method == 'POST':
        title = request.POST['title']
        overview = request.POST['overview']
        movie_duration = request.POST['movie_duration']
        release_date = request.POST['release_date']
        status = request.POST['status']
        
        if 'file-input' in request.FILES:
            poster = request.FILES['file-input']
        else:
            poster = None

        movie = Movie(
            title=title,
            overview=overview,
            movie_duration=movie_duration,
            release_date=release_date,
            status=status,
            poster=poster
        )
        movie.save()

        messages.success(request, 'Phim đã được tạo thành công!')
        return redirect('/admin/movie_list/') 
    return render(request, 'dashboard/movie_create.html') 

def movie_list(request):
    # all_movies = Movie.objects.all()
    search_query = request.GET.get('search', '')
    all_movies = Movie.objects.filter(title__icontains=search_query)

    # Set the number of movies to display per page
    if 'item' in request.GET and request.GET['item']:
        movies_per_page = request.GET['item']
    else:
        movies_per_page = 5

    # Paginate the list of movies
    paginator = Paginator(all_movies, movies_per_page)
    if 'page' in request.GET and request.GET['page']:
        page = request.GET['page']
    else:
        page = 1

    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        movies = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page
        movies = paginator.page(paginator.num_pages)
    return render(request, 'dashboard/movie_list.html', {'movies': movies})

def user_list(request):
    users = User.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})
    
def movie_edit(request, movie_id):
    current_movie = Movie.objects.get(pk=movie_id)

    date_object = current_movie.release_date
    date_str = date_object.strftime("%b. %d, %Y")
    date_object = datetime.strptime(date_str, "%b. %d, %Y").strftime("%Y-%m-%d")

    return render(request, 'dashboard/movie_edit.html',{'movie': current_movie, 'date_object': date_object})

def delete_user(request, user_id):
    row = User.objects.get(pk=user_id)
    row.delete()

def delete_movie(request, movie_id):
    row = Movie.objects.get(pk=movie_id)
    row.delete()

def print_to_pdf(request, model, fields, filename, search_query=None):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}.pdf"'
    response['Content-Transfer-Encoding'] = 'binary'

    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Setting up styles for the table
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#77a5d1'),
        ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), '#f0f0f0'),
        ('GRID', (0, 0), (-1, -1), 1, '#ffffff'),
    ])

    # Create a table and add style
    data = [fields]  # Header row
    if search_query and model == Movie:
        data += [[str(getattr(item, field)) for field in fields] for item in model.objects.filter(title__icontains=search_query)]
    else:
        data += [[str(getattr(item, field)) for field in fields] for item in model.objects.all()]

    table = Table(data)
    table.setStyle(style)

    # Draw the table on the PDF
    table.wrapOn(p, 0, 0)
    table.drawOn(p, 100, 600)

    p.showPage()
    
    p.save()

    # Get the value of the BytesIO buffer and write it to the response
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response

def export_to_excel(request, model, fields, filename, search_query=None):
    if search_query and model == Movie:
        print(search_query)
        data = model.objects.filter(title__icontains=search_query)
    else :
        data = model.objects.all()
    wb = Workbook()
    ws = wb.active
    ws.append(fields)
    for item in data:
        row_data = []
        for field in fields:
            value = getattr(item, field)

            # Check if the value is a datetime and convert to a naive datetime
            if isinstance(value, timezone.datetime):
                value = value.replace(tzinfo=None)

            row_data.append(value)

        ws.append(row_data)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
    wb.save(response)
    return response

def export_users(request):
    fields = ["username", "email", "password", "role"]
    filename = "user_data+"+ timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    return export_to_excel(request, User, fields, filename)

def export_movies(request):
    search_query = request.GET.get('search', '')
    fields = ["title", "overview", "release_date", "timestamp", "rating_count", "rating_last_updated", "rating_avg", "score", "poster_path"]
    filename = "movie_data_"+timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    if search_query:
        filename = "movie_data_q="+ search_query+timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    return export_to_excel(request, Movie, fields, filename, search_query)

def print_movies(request):
    search_query = request.GET.get('search', '')
    fields = ["title", "overview", "release_date", "timestamp", "rating_count", "rating_last_updated", "rating_avg", "score", "poster_path"]
    filename = "movie_data_"+timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    if search_query:
        filename = "movie_data_q="+ search_query+timezone.now().strftime("%Y-%m-%d %H:%M:%S")
    return print_to_pdf(request, Movie, fields, filename, search_query)

def movie_detail_admin(request, movie_id):
    current_movie = Movie.objects.get(pk=movie_id)
    return render(request, 'dashboard/movie_detail.html', {'movie': current_movie})