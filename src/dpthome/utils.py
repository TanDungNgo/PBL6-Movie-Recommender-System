from faker import Faker
import csv
import datetime
from pprint import pprint
from django.conf import settings

from faker import Faker
import requests
from requests import RequestException, HTTPError, ConnectionError, Timeout, JSONDecodeError
from django.contrib.auth.hashers import make_password

MOVIE_METADATA_CSV = settings.DATA_DIR / "movies_metadata.csv"
API_KEY = settings.API_KEY

def validate_date_str(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except:
        return None
    return date_text


def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        if 'poster_path' in data and data['poster_path']:
            poster_path = data['poster_path']
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://www.movienewz.com/img/films/poster-holder.jpg"

    except (RequestException, HTTPError, ConnectionError, Timeout, JSONDecodeError) as e:
        print(f"Error fetching data: {e}")
        return "https://www.movienewz.com/img/films/poster-holder.jpg"


def load_movie_data(limit=1):
    with open(MOVIE_METADATA_CSV, newline='',encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        dataset = []
        for i, row in enumerate(reader):
            _id = row.get("id")
            try:
                _id = int(_id)
            except:
                _id = None
            release_date = validate_date_str(row.get("release_date"))
            data = {
                "id": _id,
                "title": row.get("title"),
                "overview": row.get("overview"),
                "poster_path": fetch_poster(_id),
                "release_date": release_date,
            }
            dataset.append(data)
            if i + 1 > limit:
                break
        return dataset


def get_fake_profiles(count=10):
    fake = Faker() 
    user_data = []
    for _ in range(count):
        profile = fake.profile()
        data = {
            "username": profile.get("username"),
            "email": profile.get("mail"),
            "is_active": True,
        }
        if "name" in profile:
            fname, lname = profile.get("name").split(" ")[:2]
            data["first_name"] = fname
            data["last_name"] = lname
        fake_password = fake.password()
        hashed_password = make_password(fake_password)
        data["password"] = hashed_password
        user_data.append(data)
    return user_data