from rest_framework import viewsets
from .models import Article
from .serializer import ArticleSerializer

def crawl_and_store_articles():
    news_summary = "News Content..."
    news_keywords = ["keyword1", "keyword2"]
    new_refs = ["ref1", "ref2"]

    new_article = Article(summary = news_summary, keywords = news_keywords, refs = new_refs)

    new_article.save()

    if __name__ == "__main__":
        crawl_and_store_articles()

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer