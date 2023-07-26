from articles.models import Article
from rest_framework.decorators import api_view
from django.http import JsonResponse
from articles.serializer import ArticleSerializer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
import logging
import json

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_trend_news(request):
    total_articles = Article.objects.count()

    num_articles_to_retrieve = min(30, total_articles)

    latest_articles = Article.objects.order_by('-date')[:num_articles_to_retrieve]

    serializer = ArticleSerializer(latest_articles, many=True)

    answer = serializer.data

    return JsonResponse(answer, safe=False)

class ArticleViewSet(ViewSet):
    def list(self, request):
        queryset = Article.objects.all()
        # You can apply any filtering or ordering you need on the queryset here.
        serializer = ArticleSerializer(queryset, many=True)  # Replace YourArticleSerializer with your actual serializer
        return Response(serializer.data)