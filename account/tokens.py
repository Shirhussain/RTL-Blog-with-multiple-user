# i gonna go best on this refrence 
# https://medium.com/@frfahim/django-registration-with-confirmation-email-bb5da011e4ef

from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils import six
import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
account_activation_token = TokenGenerator()
