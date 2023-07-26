from django.contrib import admin
from django.urls import path, include
from articles.views import get_articles

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('article.urls'))
]
