# Generated by Django 4.2.7 on 2023-12-29 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_movie_idx'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
    ]