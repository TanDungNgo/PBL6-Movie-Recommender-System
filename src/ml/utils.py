import pandas as pd
import numpy as np
from zipfile import ZipFile
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pathlib
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import load_model
from django.core.files.base import File
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.conf import settings
from tensorflow.keras.layers import Embedding, multiply, concatenate, Flatten, Input, Dense
from tensorflow.keras import optimizers as opt
from keras.models import Model
import datetime
from exports.models import ExportModelNCF



from ratings.models import Rating

import pandas as pd

def export_ratings_dataset():
    BASE_DIR = settings.BASE_DIR
    ratings_exports = BASE_DIR /'data' / 'local-cdn' / 'media' / 'exports' / 'ratings' / 'latest.csv'
    ratings_df = pd.read_csv(ratings_exports)
    ratings_df['userId'] = ratings_df['userId'].astype(int)
    ratings_df['movieId'] = ratings_df['movieId'].astype(int)
    ratings_df['rating'] = ratings_df['rating'].astype(int)
    return ratings_df

def export_movies_dataset():
    BASE_DIR = settings.BASE_DIR
    movies_exports = BASE_DIR /'data' / 'local-cdn' / 'media' / 'exports' / 'movies' / 'latest.csv'
    movies_df = pd.read_csv(movies_exports)
    movies_df['trend'] = movies_df['rating_count'] * movies_df['rating_avg']
    movies_df['movieIdx'] = movies_df['movieIdx'].astype(int)
    movies_df['movieId'] = movies_df['movieId'].astype(int)
    return movies_df

def get_data_loader():
    rating_df = export_ratings_dataset()
    movies_df = export_movies_dataset()
    df = rating_df.copy()
    df['userId'] = df['userId'].astype(int)
    df['movieId'] = df['movieId'].astype(int)
    df = df.join(movies_df, on='movieId', rsuffix='_movie_df')
    df.sort_values(by=['trend'], inplace=True, ascending=False)
    df = df.copy().dropna()
    df['movieIdx'] = df['movieIdx'].astype(int)
    return df

def train_model(n_epochs=10, batch_size=200, learning_rate=0.005,embedding_size=500, verbose=True):
    data = get_data_loader()
    user_ids = data["userId"].unique().tolist()
    user2user_encoded = {x: i for i, x in enumerate(user_ids)}
    userencoded2user = {i: x for i, x in enumerate(user_ids)}
    movie_ids = data["movieIdx"].unique().tolist()
    df = data.copy()
    df["user"] = df["userId"].map(user2user_encoded)
    df["movie"] = df["movieIdx"]
    df["rating"] = data["rating"].values.astype(np.float32)
    min_rating = min(df["rating"])
    max_rating = max(df["rating"])
    df = df.sample(frac=1, random_state=42)
    x = df[["user", "movie"]].values
    y = df["rating"].apply(lambda x: (x - min_rating) / (max_rating - min_rating)).values
    train_indices = int(0.9 * df.shape[0])
    x_train, x_val, y_train, y_val = (
        x[:train_indices],
        x[train_indices:],
        y[:train_indices],
        y[train_indices:],
    )
    EMBEDDING_SIZE = embedding_size
    num_unique_users = len(user2user_encoded)
    num_unique_movies = max(movie_ids)
    users_input = Input(shape=(1,), name="users_input")
    users_embedding = Embedding(num_unique_users + 1, EMBEDDING_SIZE, name="users_embeddings")(users_input)
    users_bias = Embedding(num_unique_users + 1, 1, name="users_bias")(users_input)
    movies_input = Input(shape=(1,), name="movies_input")
    movies_embedding = Embedding(num_unique_movies + 1, EMBEDDING_SIZE, name="movies_embedding")(movies_input)
    movies_bias = Embedding(num_unique_movies + 1, 1, name="movies_bias")(movies_input)
    dot_product_users_movies = multiply([users_embedding, movies_embedding])
    input_terms = dot_product_users_movies + users_bias + movies_bias
    input_terms = Flatten(name="fl_inputs")(input_terms)
    output = Dense(1, activation="sigmoid", name="output")(input_terms)
    output = output * (max_rating - min_rating) + min_rating
    model = Model(inputs=[users_input, movies_input], outputs=output)
    opt_adam = opt.Adam(learning_rate = learning_rate)
    model.compile(optimizer=opt_adam, loss= ['mse'], metrics=['mean_absolute_error'])
    if verbose:
        model.summary()
    df_train, df_val = train_test_split(df, random_state=42, test_size=0.2, stratify=df.rating)
    print('Training model...')
    history = model.fit(
        x=[df_train.user.to_numpy(), df_train.movie.to_numpy()],
        y=df_train.rating.to_numpy(),
        batch_size=batch_size,
        epochs=n_epochs,
        verbose=1,
        validation_data=([df_val.user.to_numpy(), df_val.movie.to_numpy()],df_val.rating.to_numpy()))
    print('Training complete.')
    mean_absolute_error = [round(x, 2) for x in history.history['mean_absolute_error']]
    filename = 'neural_collaborative_filtering_{}.h5'.format(mean_absolute_error[-1])
    save_model(model, filename=filename, n_epochs=n_epochs, batch_size=batch_size, learning_rate=learning_rate, embedding_size=embedding_size)


def save_model(model, filename='neural_collaborative_filtering.h5', n_epochs=10, batch_size=200, learning_rate=0.005, embedding_size=500):
    BASE_DIR = settings.BASE_DIR
    date = datetime.datetime.now().strftime("%Y%m%d")
    file = 'data' + '/model' + '/ncf' + '/' + date + '/' + filename
    modelncf = ExportModelNCF.objects.create(
        file=file,
        n_epochs=n_epochs,
        batch_size=batch_size,
        learning_rate=learning_rate,
        embedding_size=embedding_size
    )
    filename = BASE_DIR / 'data' / 'model' / 'ncf' / date / filename
    model.save(filename)


def load_model_keras(filename='neural_collaborative_filtering.h5'):
    BASE_DIR = settings.BASE_DIR
    filename = BASE_DIR / 'data' / 'model' / filename
    loaded_model = load_model(filename)
    return loaded_model