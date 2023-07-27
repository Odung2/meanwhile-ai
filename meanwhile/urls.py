from django.contrib import admin
from django.urls import path
from articles.views import get_trend_news


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trend/', get_trend_news, name='get_trend_news')
]
