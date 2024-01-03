from django.shortcuts import render
from django.views import generic
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Movie, Genre, UserMovieHistory
import requests
from profiles.models import CustomUser as User
from datetime import datetime
import difflib
from django.core.serializers import serialize

# User = get_user_model()

# Create your views here.
API_KEY = settings.API_KEY

class MovieListView(generic.ListView):
    template_name = 'movies/list.html'
    # context -> object_list
    queryset = Movie.objects.all().order_by('-score')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        requests = self.request
        # user = requests.user
        # if user.is_authenticated:
        #     object_list = context['object_list']
        #     object_ids = [x.id for x in object_list][:20]
        #     my_ratings = user.rating_set.movies().as_object_dict(object_ids=object_ids)
        #     context['my_ratings'] = my_ratings
        genre_list = Genre.objects.all()
        context['genre_list'] = genre_list
        current_year = datetime.now().year
        year_list = list(range(current_year, current_year - 10, -1))
        year_list.append('< ' + str(current_year - 9))
        context['year_list'] = year_list
        return context
movie_list_view = MovieListView.as_view()

def get_filtered_movies(request):
    movies_per_page = 12
    selected_genre = request.GET.get('genre')
    selected_year = request.GET.get('year')
    selected_filter = request.GET.get('filter')
    if selected_genre != 'all' and selected_year != 'all':
        movies = Movie.objects.filter(genres__name=selected_genre, release_date__year=selected_year)
    elif selected_genre != 'all' and selected_year == 'all':
        movies = Movie.objects.filter(genres__name=selected_genre)
    elif selected_genre == 'all' and selected_year != 'all':
        if selected_year == '< ' + str(datetime.now().year - 9):
            movies = Movie.objects.filter(release_date__year__lt=datetime.now().year - 9)
        else:
            movies = Movie.objects.filter(release_date__year=selected_year)
    else:
        movies = Movie.objects.all()
    if selected_filter == 'featured':
        movies = movies.order_by('-score')
    elif selected_filter == 'popular':
        movies = movies.order_by('-rating_count')
    elif selected_filter == 'newest':
        movies = movies.order_by('-release_date')
    paginator = Paginator(movies, movies_per_page)
    if 'page' in request.GET and request.GET['page']:
        page = request.GET['page']
    else:
        page = 1
    try:
        movies = paginator.page(page)
    except PageNotAnInteger:
        movies = paginator.page(1)
    except EmptyPage:
        movies = paginator.page(paginator.num_pages)
    movie_html = render_to_string('movies/snippet/card_pagination.html', {'object_list': movies, 'request': request})
    response_data = {
        'status': 'success',
        'message': 'Movies retrieved successfully!',
        'movie_html': movie_html,
    }
    return JsonResponse(response_data)

def get_movies_by_genre(request):
    pass

def get_movies_by_cast(request):
    cast_id = request.GET.get('cast_id')
    filmography_url = f'https://api.themoviedb.org/3/person/{cast_id}/movie_credits?api_key={API_KEY}&language=en-US'
    response = requests.get(filmography_url)
    response.raise_for_status()
    filmography = response.json().get('cast', [])
    
    moviesofcast = []
    movie_count = 0  # Biến đếm số lượng phim đã lấy
    
    for object in filmography:
        matching_movies = Movie.objects.filter(title__iexact=object['title'])
        
        if matching_movies.exists():
            movie = {
                'id': matching_movies.first().id,
                'title': matching_movies.first().title,
                'poster_path': matching_movies.first().poster_path,
                'release_date': matching_movies.first().release_date,
                'rating_avg': matching_movies.first().rating_avg,
            }
            moviesofcast.append(movie)
            movie_count += 1
            
            if movie_count == 6:
                break
        else:
            print(f"Movie with title '{object['title']}' does not exist.")

        
    
    response_data = {
        'status': 'success',
        'message': 'Movies retrieved successfully!',
        'filmography': moviesofcast,
    }
    return JsonResponse(response_data)


class MovieDetailView(generic.DetailView):
    template_name = 'movies/detail.html'
    # context -> object -> id
    queryset = Movie.objects.all()

    def get_actor_details(self, actor_id):
        """Hàm này lấy thông tin chi tiết của diễn viên từ The Movie DB API."""
        api_key = '8265bd1679663a7ea12ac168da84d2e8'
        url = f'https://api.themoviedb.org/3/person/{actor_id}?api_key={api_key}&language=en-US'
        response = requests.get(url)
        response.raise_for_status()
        actor_details = response.json()
        return actor_details
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie_requests = self.request  # Rename 'requests' to 'movie_requests'
        user = movie_requests.user
        if user.is_authenticated:
            movie_object = context['object']
            object_ids = [movie_object.id]
            my_ratings = user.rating_set.movies().as_object_dict(object_ids=object_ids)
            if my_ratings:
                movie_id = str(movie_object.id)
                context['my_ratings'] = my_ratings.get(movie_id)
            else:
                context['my_ratings'] = 0


        movies = Movie.objects.all().order_by('-rating_avg')
        # Retrieve the movie_id from URL parameters or self.kwargs
        movie_id = self.kwargs.get('pk')  # Assuming your URL pattern uses 'pk' for the movie ID
        movie = Movie.objects.get(pk=movie_id)
        top_rated_movies = Movie.objects.all().order_by('-score')[:10]
        # related_movies = Movie.objects.filter(title__icontains=movie.title).exclude(id=movie.id)[:20]
        history_movies = []
        if user.is_authenticated:
            custom_user = User.objects.get(pk=user.id)
            user_movie_history = UserMovieHistory.objects.filter(user=custom_user).order_by('-updated')[:10]
            for history in user_movie_history:
                history_movies.append(history.movie)
        context['history_movies'] = history_movies

        # Lấy danh sách diễn viên, đạo diễn
        try:
            url_credits = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}/credits?api_key={API_KEY}&language=en-US'
            response = requests.get(url_credits)
            response.raise_for_status()
            data = response.json()
            casts = data.get('cast', [])[:8]
            directors = [crew for crew in data.get('crew', []) if crew.get('job') == 'Director']
        except requests.exceptions.RequestException as e:
            print(str(e))
            casts = []
            directors = []

        num_casts_per_row = len(casts) // 2
        first_row = casts[:num_casts_per_row]
        second_row = casts[num_casts_per_row:]

        # Lấy danh sách thể loại
        try:
            url_movie = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={API_KEY}&language=en-US'
            response = requests.get(url_movie)
            response.raise_for_status()
            data_movie = response.json()
            genres = data_movie.get('genres', [])
            countries = data_movie.get('production_countries', [])
            backdrop_path = data_movie.get('backdrop_path', [])
        except requests.exceptions.RequestException as e:
            print(str(e))
            genres = []
            countries = []
            backdrop_path = []

        context['top_rated_movies'] = top_rated_movies
        # context['related_movies'] = related_movies

        context.update({
            'movie_id': movie_id,
            'casts': casts,
            'first_row': first_row,
            'second_row': second_row,
            'genres': genres,
            'countries': countries,
            'directors': directors,
            'backdrop_path': backdrop_path,
        })
        reviews = movie.reviews.all()
        page = 5
        paginator = Paginator(reviews, page)

        context['reviews'] = paginator.get_page(1)
        
        detailed_casts = []
        for cast in context['casts']:
            actor_id = cast['id']
            actor_details = self.get_actor_details(actor_id)
            detailed_casts.append(actor_details)

        context['detailed_casts'] = detailed_casts
        return context
movie_detail_view = MovieDetailView.as_view()

class MovieVideoView(generic.DetailView):
    model = Movie
    template_name = 'movies/watch_video.html'
    # context -> object -> id
    queryset = Movie.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            movie_object = context['object']
            custom_user = User.objects.get(pk=user.id)
            user_movie_history = UserMovieHistory.objects.filter(user=custom_user, movie=movie_object).first()
            if user_movie_history:
                user_movie_history.updated = datetime.now()
                user_movie_history.save()
            else:
                user_movie_history = UserMovieHistory.objects.create(user=custom_user, movie=movie_object)
            object_ids = [movie_object.id]
            my_ratings = user.rating_set.movies().as_object_dict(object_ids=object_ids)
            if my_ratings:
                movie_id = str(movie_object.id)
                context['my_ratings'] = my_ratings.get(movie_id)
            else:
                context['my_ratings'] = 0
        movie_id = self.kwargs.get('pk')
        movie = Movie.objects.get(pk=movie_id)
        url_movie = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}/videos?api_key={API_KEY}&language=en-US'
        
        try:
            response = requests.get(url_movie)
            response.raise_for_status()
            data_movie = response.json()
            
            results = data_movie.get("results", [])
            
            if results:
                keys = [result.get("key") for result in results]
                context['keys'] = keys
        except requests.exceptions.RequestException as e:
            context['error'] = str(e)
        
        reviews = movie.reviews.all()
        page = 5
        paginator = Paginator(reviews, page)

        context['reviews'] = paginator.get_page(1)

        top_rated_movies = Movie.objects.all().order_by('-score')[:10]
        context['top_rated_movies'] = top_rated_movies

        history_movies = []
        if user.is_authenticated:
            custom_user = User.objects.get(pk=user.id)
            user_movie_history = UserMovieHistory.objects.filter(user=custom_user).order_by('-updated')[:10]
            for history in user_movie_history:
                history_movies.append(history.movie)
        context['history_movies'] = history_movies
            
        return context
movie_video_view = MovieVideoView.as_view()

def get_my_ratings(request):
    context = {}
    user = request.user
    if user.is_authenticated:
        ratings = user.rating_set.all().order_by('-timestamp')
        movie_ids = ratings.values_list('object_id', flat=True)
        movies = Movie.objects.by_id_order(movie_ids)
        movies_per_page = 12
        paginator = Paginator(movies, movies_per_page)
        if 'page' in request.GET and request.GET['page']:
            page = request.GET['page']
        else:
            page = 1
        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            movies = paginator.page(1)
        except EmptyPage:
            movies = paginator.page(paginator.num_pages)
        context['object_list'] = movies
    else:
        context['not_login'] = True
    return render(request, "movies/my_rating.html", context)

def search_movie(request):
    context = {}
    search = request.GET.get('search','')
    if search:
        movies = Movie.objects.search(search)
        movies_per_page = 12
        paginator = Paginator(movies, movies_per_page)
        if 'page' in request.GET and request.GET['page']:
            page = request.GET['page']
        else:
            page = 1
        
        try:
            movies = paginator.page(page)
        except PageNotAnInteger:
            movies = paginator.page(1)
        except EmptyPage:
            movies = paginator.page(paginator.num_pages)
        context['object_list'] = movies
    else:
        context['not_search'] = True
    return render(request, "movies/find.html", context)

def recommend(movie_name):
    movie_name = movie_name.lower()
    list_rcmd = similarity(movie_name)
    return list_rcmd


def similarity(movie_name):
    rc = rcmd(movie_name)
    return rc

def rcmd(movie_name):
    movie_name = movie_name.lower()
    try:
        data = pickle.load(open(str(settings.DATA_DIR) + '/model/movie_list.pkl','rb'))
        similarity = pickle.load(open(str(settings.DATA_DIR) + '/model/similarity.pkl','rb'))
    except:
        print("Error in pickel file")
        data, similarity = create_similarity()
    if movie_name not in data['movie_title'].unique():
        list_of_all_titles = data['movie_title'].tolist()
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles)
        if find_close_match:
            close_match = find_close_match[0]
            index = data[data['movie_title'] == close_match].index[0]
            distances = sorted(list(enumerate(similarity[index])),reverse=True,key = lambda x: x[1])
            recommended_movie_names = []
            for i in distances[1:11]:
                movie = data.iloc[i[0]].movie_title
                recommended_movie_names.append(movie)
            return recommended_movie_names
        else:
            return []
    else:
        i = data.loc[data['movie_title']==movie_name].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:11]
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l

def create_similarity():
    file = str(settings.DATA_DIR) + '/main_data.csv'
    data = pd.read_csv(file)
    # creating a count matrix
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix
    similarity = cosine_similarity(count_matrix)
    return data,similarity

def get_recommendations(request, pk):
    movie = Movie.objects.get(pk=pk)
    title = movie.title
    list_rcmd = recommend(title)
    recommend_movies = []
    for title in list_rcmd:
        matching_movies = Movie.objects.filter(title__iexact=title)
        if matching_movies.exists():
            rcmd_movie = matching_movies.first()
            recommend_movies.append(rcmd_movie)
        else:
            print(f"Movie with title '{title}' does not exist.")
    
    movie_html = render_to_string('movies/list_item.html', {'object_list': recommend_movies, 'request': request})

    response_data = {
        'status': 'success',
        'message': 'Recommendations retrieved successfully!',
        'recommend_movies': movie_html,
    }
    return JsonResponse(response_data)