from django.contrib import admin
from .models import Article, Category

#admin header change 
admin.site.site_header = "دانشیار"

def make_status_true(modeladmin, request, queryset):
    rows_updated = queryset.update(status=True)
    if rows_updated == 1:
        message_bit = "نمایش داده شد"
    else:
        message_bit = "نمایش داده شدند"
    modeladmin.message_user(request, f'{rows_updated} دسته بندی {message_bit}')
make_status_true.short_description = "دسته بندی انتخاب شده نمایش داده شود"


def make_status_false(modeladmin, request, queryset):
    rows_updated = queryset.update(status=False)
    if rows_updated == 1:
        message_bit = "نمایش داده نمی شود"
    else:
        message_bit = "نمایش داده نمی شوند"
    modeladmin.message_user(request, f'{rows_updated} دسته بندی {message_bit}')
make_status_false.short_description = "دسته بندی انتخاب شده نمایش داده نشود"





#Action is good when you want to do like a grouping work. i.e: if you wanna delete multiple row in one action
def make_published(modeladmin, request, queryset):
    rows_updated = queryset.update(status='p')
    if rows_updated == 1:
        message_bit = " منتشر شد."
    else:
        message_bit = "منتشر شدند"
    # in docutmentation of django use 'self' because it's inside a class
    # but here we don't have class instead we have model admin 
    modeladmin.message_user(request, f'{rows_updated} مقاله {message_bit}')
make_published.short_description = "انتشار مقالات انتخاب شده"

def make_draft(modeladmin, request, queryset):
    rows_updated = queryset.update(status='d')
    if rows_updated == 1:
        message_bit = "پیش نویس شد"
    else:
        message_bit = "پیش نویس شدند"
    modeladmin.message_user(request, f'{rows_updated} مقاله {message_bit}')
make_draft.short_description = " پیش نویس کردن مقالات انتخاب شده"

# if you gonna disable delete function from admin panel 
# admin.site.disable_action('delete_selected')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'position','parent','status')
    #by default we can't use boolean field here for that reason i have to 
    # i have to change it to list
    list_filter = (['status'])
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    actions = [make_status_true, make_status_false]
    
    
    
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    #here i cant't use ManyToManyField like category, i have to change it to sring first 
    #for this reason i will define a function as follows
    list_display = ('title','thumbnail_tag', "jpublish", "status",'category_to_str')
    list_filter = ('publish', 'status')
    search_fields = ('title','description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['status', '-publish']
    actions = [make_published, make_draft]

    def category_to_str(self, obj):
        #in python we someting like the this 
        #  num = [2,4,6,0,4,20]
        # [i for i in num]

        # return "،".join([category.title for category in obj.category.all()])
        """
        by defaul i tried the above line but it has some bugs like when i want to 
        hide the category that i chose نمایش داده نشود but sitll it show me on template and admin panel 
        the solution is line bellow with category_published method
        """
        return ".".join([category.title for category in obj.category.active()])
    category_to_str.short_description = "دسته بندی"

    
# admin.site.register(Article, ArticleAdmin)