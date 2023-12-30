from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from movies.models import Movie
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from openpyxl import Workbook
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle
from io import BytesIO
from datetime import datetime
from profiles.models import CustomUser
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.utils.timezone import now
# Create your views here.
User = get_user_model()
class DashboardView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'dashboard/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        end_date = now()
        start_date = datetime(2023, 1, 1)

        users_by_month = (
            User.objects
            .exclude(date_joined__isnull=True)
            .filter(date_joined__gte=start_date, date_joined__lte=end_date)
            .annotate(month=TruncMonth('date_joined'))
            .values('month')
            .annotate(user_count=Count('id'))
            .order_by('-month')
        )

        # Tạo một từ điển để lưu số lượng người dùng theo tháng
        users_by_month_dict = {entry['month'].strftime('%Y-%m'): entry['user_count'] for entry in users_by_month}

        # Tạo danh sách các tháng từ tháng 1 đến tháng 12
        month_list = [start_date.replace(day=1, month=i).strftime('%Y-%m') for i in range(1, 13)]

        # Điền đầy thông tin cho những tháng không có dữ liệu
        users_by_month_filled = [{'month': month, 'user_count': users_by_month_dict.get(month, 0)} for month in month_list]

        context['users_by_month'] = users_by_month_filled
        context['total_movies'] = Movie.objects.count()
        context['total_users'] = User.objects.count()
        users_with_last_login = User.objects.exclude(last_login__isnull=True)
        context['users_with_last_login'] = users_with_last_login
        if self.request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return JsonResponse({'users_by_month': users_by_month_filled})
        return context

    def test_func(self):
        return self.request.user.is_superuser

dashboard_view = DashboardView.as_view()

def create_movie(request):
    if request.method == 'POST':
        title = request.POST['title']
        overview = request.POST['overview']
        release_date_str = request.POST['release_date']
        poster_path = request.POST['poster_path']

        # Kiểm tra dữ liệu và thông báo lỗi nếu cần
        if not title:
            messages.error(request, 'Title is required.')
        if not overview:
            messages.error(request, 'Overview is required.')
        if not release_date_str:
            messages.error(request, 'Release Date is required.')
        if not poster_path:
            messages.error(request, 'Poster path is required.')
        else:
            try:
                # Chuyển đổi chuỗi ngày tháng nhập vào thành đối tượng datetime
                release_date = datetime.strptime(release_date_str, '%m/%d/%Y')
            except ValueError:
                messages.error(request, 'Invalid date format. Please use MM/DD/YYYY format.')

        if all([title, overview, poster_path]) and 'release_date' in locals():
            movie = Movie(
                title=title,
                overview=overview,
                release_date=release_date,
                poster_path=poster_path
            )
            movie.save()

            messages.success(request, 'Create successful!')
            return redirect('/dashboard/movie_list/')
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

def get_list_users(request):
    users = CustomUser.objects.all()
    return render(request, 'dashboard/user_list.html', {'users': users})
    
def edit_movie(request, movie_id):
    current_movie = get_object_or_404(Movie, id=movie_id)

    date_object = current_movie.release_date
    date_str = date_object.strftime("%b. %d, %Y")
    date_object = datetime.strptime(date_str, "%b. %d, %Y").strftime("%m/%d/%Y")

    if request.method == 'POST':
        title = request.POST['title']
        overview = request.POST['overview']
        release_date = request.POST['release_date']
        poster_path = request.POST['poster_path']

        # Kiểm tra dữ liệu và thông báo lỗi nếu cần
        if not title:
            messages.error(request, 'Title is required.')
        if not overview:
            messages.error(request, 'Overview is required.')
        if not release_date:
            messages.error(request, 'Release Date is required.')
        else:
            try:
                # Chuyển đổi chuỗi ngày tháng nhập vào thành đối tượng datetime
                release_date = datetime.strptime(release_date, '%m/%d/%Y')
            except ValueError:
                messages.error(request, 'Invalid date format. Please use MM/DD/YYYY format.')
        if not poster_path:
            messages.error(request, 'Poster path is required.')

        
        if not messages.get_messages(request):
            current_movie.title = title
            current_movie.overview = overview
            current_movie.release_date = release_date
            current_movie.poster_path = poster_path
            current_movie.save()

            messages.success(request, 'Update successful!')
            return redirect('/dashboard/movie_list/') 

    return render(request, 'dashboard/movie_edit.html',{'movie': current_movie, 'date_object': date_object})

def delete_user(request, user_id):
    try:
        row = User.objects.get(pk=user_id)
        row.delete()
        messages.success(request, 'User deleted successfully!')
    except Movie.DoesNotExist:
        messages.error(request, 'User does not exist')

    return redirect('user_list')

def delete_movie(request, movie_id):
    try:
        row = Movie.objects.get(pk=movie_id)
        row.delete()
        messages.success(request, 'Movie deleted successfully!')
    except Movie.DoesNotExist:
        messages.error(request, 'Movie does not exist')

    return redirect('movie_list')

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