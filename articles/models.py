from djongo import models

class Article(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    summary = models.CharField(max_length=400)
    keywords = models.CharField(max_length=300)
    refs = models.CharField(max_length=300)
    date = models.DateTimeField(auto_now=True)
    url = models.CharField(max_length=300)

    class Meta:
        db_table = 'articles'
