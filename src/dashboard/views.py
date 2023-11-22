from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import generic
from movies.models import Movie
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from openpyxl import Workbook
from django.contrib.auth import get_user_model

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
    movies = Movie.objects.all()
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

def export_to_excel(request, model, fields, filename):
    data = model.objects.all()
    wb = Workbook()
    ws = wb.active
    ws.append(fields)
    for item in data:
        row_data = [getattr(item, field) for field in fields]
        ws.append(row_data)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
    wb.save(response)
    return response

def export_users(request):
    fields = ["username", "email", "password", "role"]
    filename = "user_data"
    return export_to_excel(request, User, fields, filename)

def export_movies(request):
    fields = ["title", "overview", "release_date", "timestamp", "rating_count", "rating_last_updated", "rating_avg", "score", "poster_path"]
    filename = "movie_data"
    return export_to_excel(request, Movie, fields, filename)

def movie_detail_admin(request, movie_id):
    current_movie = Movie.objects.get(pk=movie_id)
    return render(request, 'dashboard/movie_detail.html', {'movie': current_movie})