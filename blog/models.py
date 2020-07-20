from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from extensions.utils import jalali_converter

class Article(models.Model):
    STATUS_CHOIICES = (
        ('d', 'پیش نویس'),
        ('p','انتشار'),
    )

    title = models.CharField(max_length=200, verbose_name='عنوان')
    # اگر بخوااهیم به زبان فارسی سلگ را در یوارال استفاده کنیم ، بخاطر این کار باید از الو یونی کد استفاده کنیم
    # تنها این کار کافی نیست باید در قسمت یوآرال هم از رجیکس ها استفاده کنیم زیرا پت کارساز نیست
    slug = models.SlugField(max_length=100, allow_unicode=True, unique=True, verbose_name='آدرس') 
    description = models.TextField(verbose_name='توضیحات')
    thumbnail = models.ImageField(upload_to="thumbnials", verbose_name='تصویر')
    publish = models.DateTimeField(default=timezone.now, verbose_name='زمان انتشار')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status  = models.CharField(max_length=1, choices=STATUS_CHOIICES,verbose_name='وضعیت')
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})

    
    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def jpublish(self):
        return jalali_converter(self.publish)

    