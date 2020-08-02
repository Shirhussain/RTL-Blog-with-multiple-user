from django import template
from ..models import Category

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

# we have two way to define the the 'active url' that we visite --> e.g
# {% if request.resolver_match.url_name == 'home' %}active{% endif %}
# more info try: {{request}} and {{request.resolver_match}}

# the second way is better to  define inclusion tag as follows
@register.inclusion_tag("registration/partials/link.html")
def link(request, link_name, content):
    return {
        "request": request,
        "link_name": link_name,
        "link": f"account:{link_name}",
        "content": content
    }
    