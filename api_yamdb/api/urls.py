from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ReviewViewSet, CommentViewSet

v1_router = DefaultRouter()
v1_router.register('review', ReviewViewSet, basename='review')
v1_router.register('comment', CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(v1_router.urls)),
]