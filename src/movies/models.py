from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
from django.db.models import Q, F, Sum, Case, When
from django.db.models.query import QuerySet
from ratings.models import Rating
from django.utils import timezone
import datetime
from django.db.models.signals import post_save, post_delete
from . import tasks as movies_tasks
from reviews.models import Review
from profiles.models import CustomUser as User

# Create your models here.
RATING_CALC_TIME_IN_DAYS = 3 # days

class MovieQuerySet(models.QuerySet):
    def popular(self, reverse=False):
        ordering = '-score'
        if reverse:
            ordering = 'score'
        return self.order_by(ordering)
    
    def popular_calc(self, reverse=False):
        ordering = '-score'
        if reverse:
            ordering = 'score'
        return self.annotate(score=Sum(
                F('rating_avg') * F('rating_count'),
                output_field=models.FloatField()
            )
        ).order_by(ordering)

    def needs_updating(self):
        now = timezone.now()
        days_ago = now - datetime.timedelta(days=RATING_CALC_TIME_IN_DAYS)
        return self.filter(
            Q(rating_last_updated__isnull=True)|
            Q(rating_last_updated__lte=days_ago)
        )

class MovieManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return MovieQuerySet(self.model, using=self._db)
    
    def needs_updating(self):
        return self.get_queryset().needs_updating()
    
    def search(self, query):
        lookup = (
            Q(title__icontains=query) |
            Q(overview__icontains=query) |
            Q(title__iexact=query) |
            Q(overview__iexact=query)
        )
        return self.get_queryset().filter(lookup).distinct()

    def by_id_order(self, movie_pks=[]):
        qs = self.get_queryset().filter(pk__in=movie_pks)
        maintain_order = Case(*[When(pk=pki, then=idx) for idx, pki in enumerate(movie_pks)])
        return qs.order_by(maintain_order)
    
    def count_genre_values(self):
        genre_counts = self.get_queryset().values('genres__id').annotate(count=models.Count('genres__id'))
        genre_counts = genre_counts.exclude(genres__id=None)
        genre_counts_list = [item['count'] for item in genre_counts]
        return genre_counts_list

class Movie(models.Model):
    title = models.CharField(max_length=255, unique=True)
    overview = models.TextField()
    poster_path = models.CharField(max_length=500, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True,
                                    auto_now=False, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    ratings = GenericRelation(Rating)
    rating_last_updated = models.DateTimeField(auto_now=False, auto_now_add=False,
                                                blank=True, null=True)
    rating_count = models.IntegerField(blank=True, null=True)
    rating_avg = models.DecimalField(decimal_places=2, max_digits=5,
                                        blank=True, null=True) # 5.00, 0.00
    score = models.FloatField(blank=True, null=True)
    tmdb_id = models.IntegerField(blank=True, null=True)
    idx = models.IntegerField(help_text='Position IDs for ML', blank=True, null=True)
    reviews = GenericRelation(Review)
    genres = models.ManyToManyField('Genre', blank=True)
    runtime = models.IntegerField(blank=True, null=True)
    reviews = GenericRelation(Review)

    objects = MovieManager()

    def get_genres(self):
        return self.genres.all()

    def get_genres_names(self):
        return ', '.join([genre.name for genre in self.genres.all()])

    def get_absolute_url(self):
        return f"/movies/{self.id}/"
    
    def get_video_url(self):
        return f"/movies/{self.id}/video/"
    
    def __str__(self):
        if not self.release_date:
            return f"{self.title}"
        return f"{self.title} ({self.release_date.year})"

    def rating_avg_display(self):
        now = timezone.now()
        if not self.rating_last_updated:
            return self.calculate_rating()
        if self.rating_last_updated > now - datetime.timedelta(days=RATING_CALC_TIME_IN_DAYS):
            return self.ratings_avg
        return self.calculate_rating()

    def calculate_ratings_count(self):
        return self.ratings.all().count()
    
    def calculate_ratings_avg(self):
        return self.ratings.all().avg()
    
    def calculate_rating(self, save=True):
        rating_avg = self.calculate_ratings_avg()
        rating_count = self.calculate_ratings_count()
        self.rating_avg = rating_avg
        self.rating_count = rating_count

        self.rating_last_updated = timezone.now()
        if save:
            print("saving...", self.rating_avg)
            self.save()
        return self.rating_avg

def movie_post_save(sender, instance, created, *args, **kwargs):
    if created and instance.id:
        movies_tasks.update_movie_position_embedding_idx()

post_save.connect(movie_post_save, sender=Movie)

def movie_post_delete(*args, **kwargs):
    movies_tasks.update_movie_position_embedding_idx()


post_delete.connect(movie_post_delete, sender=Movie)

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserMovieHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user.username)

    class Meta:
        verbose_name_plural = 'User Movie Histories'

def create_user_movie_history(sender, instance, created, **kwargs):
    if created:
        UserMovieHistory.objects.create(user=instance, movie=None)