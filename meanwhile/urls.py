from django.contrib import admin
from django.urls import path
from articles.views import get_trend_news, get_keyword_list, get_article_list


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/trend/', get_trend_news, name='get_trend_news'),
    path('api/keyword', get_keyword_list, name='get_keyword_list'),
    path('api/articles', get_article_list, name='get_article_list')
]
