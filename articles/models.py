from djongo import models

class Article(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    summary = models.CharField(max_length=255)
    keywords = models.JSONField(blank=True, null=True)
    refs = models.JSONField(blank=True, null=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'articles'
