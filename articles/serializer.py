from rest_framework import serializers
from .models import Article, ArticleList

class ListField(serializers.ListField):
    def to_representation(self, data):
        # Return the list with square brackets to represent it as a JSON array
        return data

    def to_internal_value(self, data):
        # Convert the comma-separated string back to a list
        return data.split(",")

class ArticleSerializer(serializers.ModelSerializer):
    # Use the custom ListField for keywords and refs
    keywords = ListField()

    class Meta:
        model = Article
        fields = ('title', 'summary', 'keywords', 'refs', 'date', 'url', 'lang')

class ArticleListSerializer(serializers.ModelSerializer):
    # Use the custom ListField for keywords and refs
    keywords = ListField()
    refs = ListField()
    title = ListField()

    class Meta:
        model = ArticleList
        fields = ('title', 'summary', 'keywords', 'refs', 'date', 'url', 'lang')
