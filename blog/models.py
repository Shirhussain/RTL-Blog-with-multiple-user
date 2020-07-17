from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

class Article(models.Model):
    STATUS_CHOIICES = (
        ('d', 'Draft'),
        ('p','Pupblished'),
    )

    title = models.CharField(max_length=200)
    # اگر بخوااهیم به زبان فارسی سلگ را در یوارال استفاده کنیم ، بخاطر این کار باید از الو یونی کد استفاده کنیم
    # تنها این کار کافی نیست باید در قسمت یوآرال هم از رجیکس ها استفاده کنیم زیرا پت کارساز نیست
    slug = models.SlugField(max_length=100, allow_unicode=True, unique=True) 
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnials")
    pubhlish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status  = models.CharField(max_length=1, choices=STATUS_CHOIICES)
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    