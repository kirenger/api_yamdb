from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoryViewSet, GenreViewSet,
    TitleViewSet,ReviewViewSet,
    CommentViewSet, UserViewSet,
    signup, token
)

router_v1 = SimpleRouter()

router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(r'review', ReviewViewSet, basename='review')
router_v1.register(r'comment', CommentViewSet, basename='comment')
router_v1.register(r'users', UserViewSet, basename='users')

auth_patterns = [
    path('signup/', signup),
    path('token/', token),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
]
