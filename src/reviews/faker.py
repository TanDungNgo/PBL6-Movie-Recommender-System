import random
from django.contrib.contenttypes.models import ContentType
from faker import Faker
from movies.models import Movie, Review
from profiles.models import CustomUser as User

fake = Faker()

def create_fake_reviews(num_reviews=100):
    users = User.objects.all()
    movies = Movie.objects.all()

    ctype = ContentType.objects.get(app_label='movies', model='movie')
    reviews = []
    for _ in range(num_reviews):
        user = random.choice(users)
        movie = random.choice(movies)
        review = Review(
            user=user,
            content = fake.paragraph(),
            content_type=ctype,
            object_id=movie.id,
        )
        reviews.append(review)
    Review.objects.bulk_create(reviews)
    print(f"{num_reviews} reviews created!")