from celery import shared_task

from django.apps import apps

from django.db.models import Window, F
from django.db.models.functions import DenseRank


@shared_task(name='task_update_movie_position_embedding_idx')
def update_movie_position_embedding_idx():
    Movie = apps.get_model('movies', "Movie")
    qs = Movie.objects.all().annotate(
        new_idx=Window(
            expression=DenseRank(),
            order_by=[F('id').asc()]
        )
    ).annotate(final_idx = F('new_idx') - 1)
    updated = 0
    for obj in qs:
        if obj.final_idx != obj.idx:
            updated += 1
            obj.idx = obj.final_idx
            obj.save()
    print(f"Updated {updated} movie idx fields")

import requests
def fakeGenre(start_batch):
    from .models import Movie, Genre
    api_key = '8265bd1679663a7ea12ac168da84d2e8'
    movies = Movie.objects.all()

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