from django.db import models

# Create your models here.
class Blog(models.Model):
    id = models.BigIntegerField(primary_key=True, serialize=True)
    title = models.TextField()
    content = models.TextField()
    author = models.TextField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

