from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import Textarea
from django.forms import ModelForm
from library import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('username', 'email', 'bio', 'profile_pic')


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm):
        model = CustomUser
        fields = UserChangeForm.Meta.fields


#  in case i want to change only bio and profile pic
class CustomUserChangeOnlyTwoForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('bio', 'profile_pic')
        widgets = {
            'bio': Textarea(attrs={'cols': 80, 'rows': 4}),
        }
