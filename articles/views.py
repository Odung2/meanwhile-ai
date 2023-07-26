from .models import Article
from .serializer import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse

@api_view(['GET'])
def get_trend_news(request):
    total_articles = Article.objects.count()

    num_articles_to_retrieve = 30 if total_articles>=30 else total_articles

    latest_articles = Article.objects.order_by('-date')[:num_articles_to_retrieve].values()

    article_list = list(latest_articles)
    
    return JsonResponse(article_list, safe=False)