from django.db import models
from django.utils import timezone

class Article(models.Model):
    STATUS_CHOIICES = (
        ('d', 'Draft'),
        ('p','Pupblished'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, allow_unicode=True, unique=True)  #editable=True
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnials")
    pubhlish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status  = models.CharField(max_length=1, choices=STATUS_CHOIICES)
    
