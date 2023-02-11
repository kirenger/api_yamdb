from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.routers import NoPutRouter

from api.views import (
    CategoryViewSet, GenreViewSet,
    TitleViewSet, ReviewViewSet,
    CommentViewSet, UserViewSet,
    signup, token
)

router_v1 = SimpleRouter()
router_v2 = NoPutRouter()

router_v1.register(r'titles', TitleViewSet, basename='titles')
router_v1.register(r'genres', GenreViewSet, basename='genres')
router_v1.register(r'categories', CategoryViewSet, basename='categories')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router_v2.register(r'users', UserViewSet, basename='users')

auth_patterns = [
    path('signup/', signup),
    path('token/', token),
    path('', include('djoser.urls')),
    path('', include('djoser.urls.jwt')),
]

urlpatterns = [
    path('v1/auth/', include(auth_patterns)),
    path('v1/', include(router_v1.urls)),
    path('v1/', include(router_v2.urls)),
]
