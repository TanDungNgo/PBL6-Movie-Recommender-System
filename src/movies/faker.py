import requests
from .models import Movie, Genre
from profiles.models import CustomUser as User
from django.utils import timezone
import random

def generateGenreMovies(start_batch):
    api_key = '8265bd1679663a7ea12ac168da84d2e8'
    # movies = Movie.objects.all()
    movies =  Movie.objects.filter(genres__isnull=True)

    batch_size = 50
    num_batches = (movies.count() + batch_size - 1) // batch_size

    for batch_num in range(start_batch, num_batches):
        print(f'Processing batch {batch_num + 1} of {num_batches}')
        start_index = batch_num * batch_size
        end_index = (batch_num + 1) * batch_size

        current_batch = movies[start_index:end_index]

        for movie in current_batch:
            api_url = f'https://api.themoviedb.org/3/movie/{movie.tmdb_id}?api_key={api_key}&language=en-US'
            response = requests.get(api_url)
            data = response.json()

            genres = data.get('genres', [])

            for genre_data in genres:
                genre_name = genre_data.get('name')
                if genre_name:
                    genre, created = Genre.objects.get_or_create(name=genre_name)
                    movie.genres.add(genre)

            time = data.get('runtime')
            if time:
                movie.runtime = time
            movie.save()

def movies_without_genres():
    movies = Movie.objects.filter(genres__isnull=True)
    print(movies.count())
    for movie in movies:
        print(movie.title)

def generateDatejoined():
    users = User.objects.all()
    for user in users:
        print(f'Processing batch {user.id} of {users.count()}')
        year = user.date_joined.year
        random_date = timezone.now().replace(year=year, day=random.randint(1, 28), month=random.randint(1, 12))
        user.date_joined = random_date
        user.save()