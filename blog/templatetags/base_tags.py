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
    