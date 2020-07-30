from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

    # If you’re starting a new project, it’s highly recommended to set up a custom user model,
    # even if the default User model is sufficient for you. This model behaves identically to the default user model,
    # but you’ll be able to customize it in the future if the need arises, 
    # for example you wanna add 'email addres' or phone number

class User(AbstractUser):
    """
    here we don't need to rewrite every filed just add wat you want to 
    append to the previous use fields 
    """
    is_author = models.BooleanField(default=False, verbose_name="وضعیت نویسندگی")
    special_user = models.DateTimeField(default=timezone.now, verbose_name="کاربر ویژه")

    def is_special_user(self):
        if self.special_user > timezone.now():
            return True
        else:
            return False

    # in admin if you wanna show 'True/False' to 'green and red' button sow use this line 
    is_special_user.boolean = True
    is_special_user.short_description = "وضعیت کابر ویژه"