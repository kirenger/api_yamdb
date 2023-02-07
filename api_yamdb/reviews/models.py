from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name='titles'
    )
    genre = models.ForeignKey(
        Genre, on_delete=models.SET_NULL, related_name='genres'
    )
    name = models.CharField(max_length=256)
    year = models.IntegerField()
    description = models.TextField()
