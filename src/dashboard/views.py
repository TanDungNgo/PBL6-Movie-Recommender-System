from collections import defaultdict
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
from profiles.models import CustomUser as User
from django.db.models import Count, Value
from django.db.models.functions import ExtractMonth, ExtractYear
from ratings.models import Rating
from django.db.models.functions import Coalesce
from reviews.models import Review
# Create your views here.
# User = get_user_model()
class DashboardView(LoginRequiredMixin, UserPassesTestMixin, generic.TemplateView):
    template_name = 'dashboard/dashboard.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['total_movies'] = Movie.objects.count()
        context['total_users'] = User.objects.count()
        users_with_last_login = User.objects.exclude(last_login__isnull=True)
        context['users_with_last_login'] = users_with_last_login
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
    users = User.objects.all()
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

def users_by_month(request):
    user_counts = User.objects.annotate(
        year=ExtractYear('date_joined'),
        month=ExtractMonth('date_joined')
    ).values('year', 'month').annotate(count=Count('id'))

    # Chuyển kết quả thành một danh sách để trả về dưới dạng JSON
    result = list(user_counts)

    return JsonResponse(result, safe=False)

def movies_by_genre(request):
    genre_counts = Movie.objects.count_genre_values()

    return JsonResponse({'moviesCount': genre_counts})

def get_movie_review_counts(request):
    search_query = request.GET.get('search', '')
    movies_info = (
        Movie.objects
        .values('id', 'title', 'rating_count', 'rating_avg')
        .filter(title__icontains=search_query)
    )
    
    review_counts = (
        Review.objects
        .values('object_id')
        .annotate(review_count=Count('object_id'))
        .exclude(object_id=None)
    )

    result_list = []
    for movie_info in movies_info:
        movie_id = movie_info['id']
        movie_title = movie_info['title']
        rating_count = movie_info['rating_count']
        rating_avg = movie_info['rating_avg']

        rating_count = 0 if rating_count is None else rating_count
        rating_avg = 0 if rating_avg is None else rating_avg

        review_count = next(
            (item['review_count'] for item in review_counts if item['object_id'] == movie_id),
            0
        )

        result_list.append({
            'id': movie_id,
            'title': movie_title,
            'review_count': review_count,
            'rating_count': rating_count,
            'rating_avg': rating_avg
        })

    # Phân trang
    items_per_page = request.GET.get('item', 10)

    # Paginate the list of results
    paginator = Paginator(result_list, items_per_page)
    page = request.GET.get('page', 1)

    try:
        paginated_result = paginator.page(page)
    except PageNotAnInteger:
        # If the page parameter is not an integer, show the first page
        paginated_result = paginator.page(1)
    except EmptyPage:
        # If the page is out of range, deliver the last page
        paginated_result = paginator.page(paginator.num_pages)

    return render(request, 'dashboard/rating_review.html', {'movies': paginated_result})

def get_movie_review_details(request, movie_id):
    review_detail = (
        Review.objects
        .filter(object_id = movie_id)
        .values('id', 'content', 'object_id', 'user_id', 'timestamp', 'sentiment')
    )

    if review_detail.exists():
        movies_info = (
            Movie.objects
            .filter(id=movie_id)
            .values('id', 'title')
        )

        users_info = (
            User.objects
            .filter(id__in=[item['user_id'] for item in review_detail])
            .values('id', 'username')
        )

        result_list = []
        for review_item in review_detail:
            user_id = review_item['user_id']
            title_movie = movies_info[0]['title']
            user_info = next((item for item in users_info if item['id'] == user_id), None)
            username = user_info['username'] if user_info else None

            result_list.append({
                'id': review_item['id'],
                'content': review_item['content'],
                'title_movie': title_movie,
                'username': username,
                'timestamp': review_item['timestamp'].strftime("%b. %d, %Y"),
                'sentiment':  review_item.get('sentiment', None)
            })
    
        return render(request, 'dashboard/review_table.html', {'results': result_list, 'title_movie': title_movie})
    else:
        return render(request, 'dashboard/empty_page.html')
    
def get_movie_rating_details(request, movie_id):
    rating_detail = (
        Rating.objects
        .filter(object_id = movie_id)
        .values('id', 'value', 'object_id', 'user_id', 'timestamp')
    )

    if rating_detail.exists():
        movies_info = (
            Movie.objects
            .filter(id=movie_id)
            .values('id', 'title')
        )

        users_info = (
            User.objects
            .filter(id__in=[item['user_id'] for item in rating_detail])
            .values('id', 'username')
        )

        result_list = []
        for review_item in rating_detail:
            user_id = review_item['user_id']
            title_movie = movies_info[0]['title']
            user_info = next((item for item in users_info if item['id'] == user_id), None)
            username = user_info['username'] if user_info else None

            result_list.append({
                'id': review_item['id'],
                'value': review_item['value'],
                'title_movie': title_movie,
                'username': username,
                'timestamp': review_item['timestamp'].strftime("%b. %d, %Y")
            })

        # Phân trang
        items_per_page = request.GET.get('item', 10)
        paginator = Paginator(result_list, items_per_page)
        page = request.GET.get('page', 1)

        try:
            paginated_result = paginator.page(page)
        except PageNotAnInteger:
            paginated_result = paginator.page(1)
        except EmptyPage:
            paginated_result = paginator.page(paginator.num_pages)


        rating_count = defaultdict(int)  
        for review_item in rating_detail:
            value = review_item['value']
            rating_count[value] += 1
    
        sorted_rating_count = dict(sorted(rating_count.items(), key=lambda item: item[0], reverse=True))  
        
        return render(request, 'dashboard/rating_table.html', {'results': paginated_result, 'title_movie': title_movie, 'rating_count': sorted_rating_count})
    else:
        return render(request, 'dashboard/empty_page.html')
    
def get_rating_count(request, movie_id):
    rating_counts = (
        Rating.objects
        .filter(object_id = movie_id)
        .values('value')
        .annotate(count=Count('value'))
    )

    # Tính tổng số đánh giá
    total_ratings = sum(entry['count'] for entry in rating_counts)

    # Tạo dictionary để lưu trữ phần trăm cho mỗi giá trị
    percentage_count = defaultdict(float)

    # Tính phần trăm và lưu vào dictionary
    for entry in rating_counts:
        value = entry['value']
        count = entry['count']
        percentage = (count / total_ratings) * 100
        percentage_count[value] = round(percentage, 2) 

    for value in [1, 2, 3, 4, 5]:
        if value not in percentage_count:
            percentage_count[value] = 0.0

    print(percentage_count)
    result = {'total_ratings': total_ratings, 'percentage_count': dict(percentage_count)}
    return JsonResponse(result, safe=False)
