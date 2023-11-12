from django.core.management.base import BaseCommand, CommandParser
from django.contrib.auth import get_user_model

from movies.models import Movie
from dpthome import utils as dpthome_utils

User = get_user_model() 

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count",nargs='?',
                            default=10, type=int)
        parser.add_argument("--movies", 
                            action="store_true", default=False)
        parser.add_argument("--users", 
                            action="store_true", default=False)
        parser.add_argument("--show-total", 
                            action="store_true", default=False)
    def handle(self, *args, **options):
        count = options.get('count')
        show_total = options.get('show_total')
        load_movies = options.get('movies')
        generate_users = options.get('users')
        if load_movies:
            movie_dataset = dpthome_utils.load_movie_data(limit = count)
            movies_new = [Movie(**data) for data in movie_dataset]
            movie_bulk = Movie.objects.bulk_create(movies_new
                                    , ignore_conflicts=True)
            print(f"Created {len(movie_bulk)} movies")
            if show_total:
                print(f"Total movies: {Movie.objects.count()}")
        if generate_users:
            profiles = dpthome_utils.get_fake_profiles(count = count)
            
            new_users = []
            for profile in profiles:
                new_users.append(User(**profile))
            user_bulk = User.objects.bulk_create(new_users
                                    , ignore_conflicts=True)
            print(f"Created {len(user_bulk)} users")
            if show_total:
                print(f"Total users: {User.objects.count()}")
