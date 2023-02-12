from datetime import datetime

from django.db import models
from django.core.validators import (
    MaxValueValidator, MinValueValidator
)

from users.models import User


class Category(models.Model):
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Название категории'
    )
    slug = models.SlugField(unique=True, max_length=50)


class Genre(models.Model):
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(unique=True, max_length=50)


class Title(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Название категории'
    )
    genre = models.ManyToManyField(
        Genre, related_name='genres'
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения'
    )
    year = models.IntegerField(
        db_index=True,
        validators=[MaxValueValidator(datetime.now().year)],
        verbose_name='Год издания'
    )
    description = models.TextField()


class Review(models.Model):
    """Модель отзывов."""
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews')
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True
    )
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг произведения',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
    )

    class Meta:
        ordering = ('-pub_date',)
        constraints = (
            models.UniqueConstraint(
                fields=('title', 'author',),
                name='unique_author_title'
            ),
        )

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    """Модель комментириев."""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
