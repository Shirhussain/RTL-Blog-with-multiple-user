from django.contrib import admin
from .models import Article, Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'position','status')
    #by default we can't use boolean field here for that reason i have to 
    # i have to change it to list
    list_filter = (['status'])
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    
    
    
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    #here i cant't use ManyToManyField like category, i have to change it to sring first 
    #for this reason i will define a function as follows
    list_display = ('title', "jpublish", "status",'category_to_str')
    list_filter = ('publish', 'status')
    search_fields = ('title','description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['status','-publish']

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
        return ".".join([category.title for category in obj.category_published()])
    category_to_str.short_description = "دسته بندی"

    
# admin.site.register(Article, ArticleAdmin)