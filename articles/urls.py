from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet
from articles.views import get_articles

router = DefaultRouter()
router.register(r'article', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/articles/', get_articles, name='get_articles')
]