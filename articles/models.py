from django.db import models
from djongo.models.fields import ListField

class Article:
    article_id = models.IntegerField(auto_created=True, primary_key=True)
    summary = models.CharField()
    keywords = ListField()
    refs = ListField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.keywords
    
    class Meta:
        db_table = 'meanwhile_ai_db'

    