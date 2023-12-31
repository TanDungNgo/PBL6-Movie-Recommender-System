# Generated by Django 4.2.7 on 2023-12-29 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0008_genre'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='genres',
            field=models.ManyToManyField(blank=True, to='movies.genre'),
        ),
        migrations.AddField(
            model_name='movie',
            name='runtime',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
