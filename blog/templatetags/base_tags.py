from django import template
from ..models import Category, Article
from django.db.models import Count, Q
from datetime import datetime, timedelta


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
@register.inclusion_tag("blog/partial/popular_articles.html")
def popular_articles():
    last_month = datetime.today()-timedelta(days=30)
    return {
        'popular_articles': Article.objects.annotate(
            # wiht lookup '__' you can access to field of another linked table
            count=Count('hits', filter=Q(articlehit__created__gt=last_month))
            ).order_by('-count', '-publish')[:5]
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
    