from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.html import format_html
from account.models import User

from extensions.utils import jalali_converter


#by default if i wanna change the status of an article to draft but in still i can see 
#that it's show us on the tempalte also i can't use "filter()" in template 
# the solution is that i have to use "managers"
class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status='p')

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)

class Category(models.Model):
    # wanna add subcategory as well 
    parent = models.ForeignKey('self', default=None, null=True,blank=True,on_delete=models.SET_NULL, related_name="children", verbose_name="زیردسته")
    title = models.CharField(max_length=200, verbose_name='عنوان دسته بندی')
    slug = models.SlugField(max_length=200, allow_unicode=True, unique=True, verbose_name='آدرس دسته بندی')
    status = models.BooleanField(default=True, verbose_name='آیا نمایش داده شود؟')
    position = models.IntegerField(verbose_name='مقام')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        # i use parent__id instead of just parent to prevent infinite loop 
        ordering = ['parent__id','position']

    def __str__(self):
        return self.title
        
    objects = CategoryManager()

class Article(models.Model):
    STATUS_CHOIICES = (
        ('d', 'پیش نویس'),
        ('p','انتشار'),
    )

    author = models.ForeignKey(User,null=True, on_delete=models.SET_NULL, related_name="articles", verbose_name="نویسنده")
    title = models.CharField(max_length=200, verbose_name='عنوان')
    # اگر بخوااهیم به زبان فارسی سلگ را در یوارال استفاده کنیم ، بخاطر این کار باید از الو یونی کد استفاده کنیم
    # تنها این کار کافی نیست باید در قسمت یوآرال هم از رجیکس ها استفاده کنیم زیرا پت کارساز نیست
    slug = models.SlugField(max_length=100, allow_unicode=True, unique=True, verbose_name='آدرس') 
    category = models.ManyToManyField(Category, related_name= "articles" , verbose_name='دسته بندی')
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

    objects = ArticleManager()

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"
        ordering = ['-publish']
    
    def jpublish(self):
        return jalali_converter(self.publish)
    jpublish.short_description = "زمان انتشار"
    

        
    def thumbnail_tag(self):
        return format_html(f"<img width=100 style='border-radius: 4px;' src='{self.thumbnail.url}'>")
    thumbnail_tag.short_description = "عکس"

    # if i wnna use category to str in my template nad admin for both so i sould wirte down her
    # if i wanna use jus in admin i could use in Admin with (obj) not self  like this:
    # def cateogry_to_str(self,obj):
    def category_to_str(self):
        #in python we someting like the this 
        #  num = [2,4,6,0,4,20]
        # [i for i in num]

        # return "،".join([category.title for category in obj.category.all()])
        """
        by defaul i tried the above line but it has some bugs like when i want to 
        hide the category that i chose نمایش داده نشود but sitll it show me on template and admin panel 
        the solution is line bellow with category_published method
        """
        return ".".join([category.title for category in self.category.active()])
    category_to_str.short_description = "دسته بندی"