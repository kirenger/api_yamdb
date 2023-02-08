from django.urls import include, path
from rest_framework.routers import SimpleRouter

from api.views import (
    CategoryViewSet, GenreViewSet,
    TitleViewSet, signup, token,
    ReviewViewSet, CommentViewSet
)

router_v1 = SimpleRouter()

router_v1.register(r'titles', TitleViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'review', ReviewViewSet,)
router_v1.register(r'comment', CommentViewSet)

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
