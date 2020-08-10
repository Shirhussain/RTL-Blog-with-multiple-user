from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserForm(forms.ModelForm):
    # here i wanna overwrite the __init__ method to prevent the use from editing the whole fields
    # author just can edite their name and last name, other thing should be disabled
    def __init__(self, *args, **kwargs):
        # i have to take the use and then remove it 'pop' afther that because of superuser
        user = kwargs.pop('user')
        super(UserForm, self).__init__(*args, **kwargs)
        
        if not user.is_superuser:
            self.fields['username'].help_text = None
            self.fields['username'].disabled = True
            self.fields['email'].disabled = True
            self.fields['special_user'].disabled = True
            self.fields['is_author'].disabled = True

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'special_user', 'is_author']

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')