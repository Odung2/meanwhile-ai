from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet
from articles.views import get_trend_news

router = DefaultRouter()
router.register(r'article', ArticleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('trend/', get_trend_news, name='get_trend_news')
]