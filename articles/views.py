from django.http import JsonResponse
from .models import Article
from articles.serializer import ArticleSerializer
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from django.core import serializers
import traceback
import logging
import os
import subprocess

# Get the current file path of views.py
current_file_path = os.path.abspath(__file__)

# Get the parent directory of views.py (i.e., meanwhile-ai/articles/)
articles_directory = os.path.dirname(current_file_path)

# Move up one more directory to reach the meanwhile-ai/ folder
meanwhile_ai_directory = os.path.dirname(articles_directory)

# Construct the relative path to the article_search.txt file in the meanwhile-ai/data/raw_data/ folder
article_search_file_path = os.path.join(meanwhile_ai_directory, 'data', 'raw_data', 'article_search.txt')

timeline_search_file_path = os.path.join(meanwhile_ai_directory, 'data', 'raw_data', 'timeline_search.txt')

korean_keyword_path = os.path.join(meanwhile_ai_directory, 'data', 'processed_data', '7_timeline_keyword', 'timeline_keyword_ko.txt')

english_keyword_path = os.path.join(meanwhile_ai_directory, 'data', 'processed_data', '7_timeline_keyword', 'timeline_keyword_en.txt')

english_final_path = os.path.join(meanwhile_ai_directory, 'data', 'processed_data', '8_timeline_final', 'timeline_en_final.txt')

korean_final_path = os.path.join(meanwhile_ai_directory, 'data', 'processed_data', '8_timeline_final', 'timeline_ko_final.txt')

keyword_shell_path = os.path.join(meanwhile_ai_directory, 'scripts', 'keyword_script.sh')

timeline_shell_path = os.path.join(meanwhile_ai_directory, 'scripts', 'timeline_script.sh')

article_shell_path = os.path.join(meanwhile_ai_directory, 'scripts', 'article_script.sh')

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
    
@api_view(['GET'])
def get_keyword_list(request):
    input_text = request.GET.get('query', '')
    korean_keywords = ""
    english_keywords = ""

    with open(timeline_search_file_path, 'w') as file:
        file.write(input_text)
    
    result = subprocess.run(["bash", keyword_shell_path], capture_output=True, text=True)

    with open(korean_keyword_path, 'r') as file:
        korean_keywords = file.read()

    with open(english_keyword_path, 'r') as file:
        english_keywords = file.read()

    response_data = {
        "korean_keywords": korean_keywords,
        "english_keywords": english_keywords
    }

    # Return the response data as JSON
    return JsonResponse(response_data, safe=False)

@api_view(['GET'])
def get_article_list(request):
    korean = request.GET.get('korean', '')
    english = request.GET.get('english', '')

    with open(korean_keyword_path, 'w') as file:
        file.write(korean)

    with open(english_keyword_path, 'w') as file:
        file.write(english)

    result = subprocess.run(["bash", timeline_shell_path], capture_output=True, text=True)

    with open(korean_final_path, 'r') as file:
        korean_final = file.read()

    with open(english_final_path, 'r') as file:
        english_final = file.read()


    response_data = {
        "korean_final": korean_final,
        "english_final": english_final
    }

    return JsonResponse(response_data, safe=False)