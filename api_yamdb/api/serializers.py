from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from datetime import datetime as dt

from reviews.models import Category, Genre, Title, User, Comment, Review
from api.validators import validate_username, validate_email


class CategorySerializer(serializers.ModelSerializer):
    class Meta():
        fields = (
            'name',
            'slug',
        )
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta():
        fields = (
            'name',
            'slug',
        )
        model = Genre


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year', 'description', 'rating', 'category', 'genre'
        )

    def validate_year(self, value):
        year_today = dt.date.today().year
        if value > year_today:
            raise serializers.ValidationError('Будущее еще не наступило!)')
        return value


class TitlePostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(),
        many=True
    )

    class Meta():
        fields = '__all__'
        model = Title


class TokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField(allow_blank=False)
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[validate_username]
    )

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        confirmation_code = default_token_generator.make_token(user)
        if str(confirmation_code) != data['confirmation_code']:
            raise ValidationError('Неверный код подтверждения')
        return data


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        max_length=254,
        allow_blank=False,
        validators=[validate_email]
    )
    username = serializers.CharField(
        max_length=150,
        allow_blank=False,
        validators=[validate_username]
    )

    class Meta:
        model = User
        fields = ('email', 'username')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Вы можете добавить только один отзыв')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев."""
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text', read_only=True
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'review', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )


class UserMeSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        read_only_fields = ('role',)
