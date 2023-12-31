# Generated by Django 4.2.7 on 2024-01-01 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_rename_country_customuser_address'),
        ('movies', '0009_movie_genres_movie_runtime_alter_genre_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserMovieHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated', models.DateTimeField(auto_now=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profiles.customuser')),
            ],
            options={
                'verbose_name_plural': 'User Movie Histories',
            },
        ),
    ]
