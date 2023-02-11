from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.db.models import Avg
from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from django.conf import settings
from reviews.models import Category, Genre, Title, Review
from api.serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer, TitlePostSerializer,
    SignUpSerializer, TokenSerializer, CommentSerializer, ReviewSerializer,
    UserSerializer, UserMeSerializer
)
from api.permissions import (
    IsAdminOrReadOnly, ReviewPermission, IsAdminOnlyPermission,
    SelfEditUserOnlyPermission
)
from api.filters import FilterTitle
from users.models import User


class CreateListDestroy(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CreateListDestroy):
    queryset = Category.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_fields = ('name', 'slug')
    search_fields = ('name', 'slug')


class GenreViewSet(CreateListDestroy):
    queryset = Genre.objects.all()
    pagination_class = LimitOffsetPagination
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ('name', 'slug')
    filterset_fields = ('name', 'slug')


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    filterset_class = FilterTitle
    search_fields = ('name', 'year', 'genre__slug', 'category__slug')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleSerializer
        return TitlePostSerializer

    def get_queryset(self):
        if self.action in ('list', 'retrieve'):
            queryset = (
                Title.objects.prefetch_related('reviews').all().
                annotate(rating=Avg('reviews__score')).order_by('name')
            )
            return queryset
        return Title.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = (ReviewPermission,)

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для комментариев."""
    serializer_class = CommentSerializer
    permission_classes = (ReviewPermission,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review, id=self.kwargs['review_id'],
            title=self.kwargs['title_id']
        )
        serializer.save(author=self.request.user, review=review)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для юзера."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    permission_classes = (IsAdminOnlyPermission,)

    @action(
        methods=['get', 'patch'], detail=False,
        url_path='me', permission_classes=(SelfEditUserOnlyPermission,)
    )
    def me(self, request):
        if request.method == 'GET':
            user = User.objects.get(username=request.user)
            serializer = self.get_serializer(user)
            return Response(serializer.data)

        user = User.objects.get(username=request.user)
        serializer = UserMeSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = SignUpSerializer(data=request.data)
    if User.objects.filter(
        username=request.data.get('username'), email=request.data.get('email')
    ).exists():
        return Response(request.data, status=status.HTTP_200_OK)
    else:
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(
            username=request.data.get('username'),
            email=request.data.get('email')
        )
        conformation_code = default_token_generator.make_token(user)
        send_mail(
            f'Привет, {str(user.username)}! Твой код находится тут!',
            conformation_code,
            settings.EMAIL_FOR_AUTH_LETTERS,
            [request.data['email']],
            fail_silently=True
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(User, username=request.data['username'])
    confirmation_code = request.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = get_tokens_for_user(user)
        response = {'token': str(token['access'])}
        return Response(response, status=status.HTTP_200_OK)
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )
