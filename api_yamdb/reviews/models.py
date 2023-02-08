from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


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


class Review(models.Model):
    """Модель отзывов"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Пользователь'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв'
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
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date', ]
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review',
            ),
        ]


class Comment(models.Model):
    """Модель комментириев"""
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
