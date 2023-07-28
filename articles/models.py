from djongo import models

class Article(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    title = models.TextField(null=True)
    summary = models.TextField()
    keywords = models.TextField()
    refs = models.TextField()
    date = models.DateTimeField()
    url = models.TextField()
    lang = models.IntegerField(null=True)

    class Meta:
        db_table = 'articles'

class ArticleList(models.Model):
    title = models.TextField(null=True)
    summary = models.TextField()
    keywords = models.TextField()
    refs = models.TextField()
    date = models.DateTimeField()
    url = models.TextField()
    lang = models.IntegerField(null=True)

    class Meta:
        db_table = 'articles_list'