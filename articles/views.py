from django.http import JsonResponse
from .models import Article
from articles.serializer import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from django.core import serializers
import traceback
import logging

@api_view(['GET'])
def get_trend_news(request):
    try:
        total_articles = Article.objects.count()
        num_articles_to_retrieve = min(30, total_articles)
        latest_articles = Article.objects.order_by('-date')[:num_articles_to_retrieve]
        serializer = ArticleSerializer(latest_articles, many=True)
        data = serializer.data

        return JsonResponse(data, safe=False)

    except Article.DoesNotExist:
        # If no articles are found, return an empty list
        return JsonResponse([], safe=False)

    except APIException as e:
        # Handle Django REST framework API exceptions
        return JsonResponse({'error': str(e)}, status=e.status_code)

    except Exception as e:
        logging.info(e)
        # Handle other exceptions
        return JsonResponse({'error': str(e)}, status=500)
