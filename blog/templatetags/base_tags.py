from django import template
from ..models import Category, Article
from django.db.models import Count, Q
from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType


register = template.Library()

@register.simple_tag
def title():
    return "شیرحسین دانشیار"



    """بخاطر ایجاد کتگوری در نوبار ما باید تگ های اختصاصی ایجاد کنیم در غیر این صورت
    باید بسیاری از کد ها را چندین بار بنوسیم فقط تکرار کدها می شود و پروژه ما سنگین می شود
    """
@register.inclusion_tag("blog/partial/category_navbar.html")
def category_navbar():
    return {
        'category': Category.objects.filter(status=True)
    }

# annotate = برای برقرار کردن ارتباط بین جدول ها استفاده می شود، مثلا ممکن است تعداد کتاب را در انتشارات حساب کرد
# aggregate = برای حساب کردن در خود یک جدول استفاده می شود 
@register.inclusion_tag("blog/partial/sidebar.html")
def popular_articles():
    last_month = datetime.today()-timedelta(days=30)
    return {
        'articles': Article.objects.annotate(
            # wiht lookup '__' you can access to field of another linked table
            count=Count('hits', filter=Q(articlehit__created__gt=last_month))
            ).order_by('-count', '-publish')[:5],
        'title': 'مقالات پر بازدید ماه'
    }

@register.inclusion_tag("blog/partial/sidebar.html")
def hot_articles():
    last_month = datetime.today()-timedelta(days=30)
    content_type_id = ContentType.objects.get(app_label='blog', model='article').id
    return {
        'articles': Article.objects.annotate(
            # for comment application we have content_type_id for a references to connected model
            # otherwise we don't know to which model our comment is connected, this proses is done through Generic relation
            # you can statically also write just find from table like at first i have don so i.e: '3' 
            count=Count('comments', filter=Q(comments__posted__gt=last_month) and Q(comments__content_type_id=content_type_id))
            ).order_by('-count', '-publish')[:5],
        'title': 'مقالات داغ ماه'
    }

# we have two way to define the the 'active url' that we visite --> e.g
# {% if request.resolver_match.url_name == 'home' %}active{% endif %}
# more info try: {{request}} and {{request.resolver_match}}

# the second way is better to  define inclusion tag as follows
@register.inclusion_tag("registration/partials/link.html")
def link(request, link_name, content, classes):
    return {
        "request": request,
        "link_name": link_name,
        "link": f"account:{link_name}",
        "content": content,
        "classes": classes
    }
    