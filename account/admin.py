from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from.models import User

""" 
if you wanna see how i'm defining my own fields to dajngo admin you casa see 
this path that how django it self tefine that --> /lib/python3.8/site-packages/django/contrib/auth/admin.py 
like the follwing i do it's ok and will append to the admin  
UserAdmin.fieldsets += (
    ("فیلدهای اختصاصی خودم",{'fields':('is_author','special_user')}),
)
"""

# but i wanna show you hwo to add in sdie some speacial indexes  e.g in i gonna add to permissian fiels
# if you wanna know how it's work again go to mintioned admin linke

UserAdmin.fieldsets[2][1]['fields'] = (
    'is_active',
    'is_staff',
    'is_superuser',
    'is_author',
    # her i added my own fields 
    'special_user',
    'groups',
    'user_permissions'
)

# if you want to display like other field list_display in admin so here we go 
UserAdmin.list_display += ('is_author', 'is_special_user')  #if wana show 'True/False' use is_special 
# but if you wanna show date and time use just 'special_user'



admin.site.register(User, UserAdmin)