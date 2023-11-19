from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ratings.tasks import task_update_movie_ratings
# from movies.tasks import task_caculate_movie_rating

User = get_user_model() 

class Command(BaseCommand):
    
    def handle(self, *args, **options):
        task_update_movie_ratings()
        # task_caculate_movie_rating(all=all, count=count)