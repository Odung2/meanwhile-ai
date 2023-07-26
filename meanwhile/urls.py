from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from articles.views import ArticleViewSet, get_trend_news

router = DefaultRouter()
router.register(r'article', ArticleViewSet, basename='article')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/trend/', get_trend_news, name='get_trend_news')
]
