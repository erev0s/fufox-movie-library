from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from allauth.account.adapter import DefaultAccountAdapter


class CustomUser(AbstractUser):
    bio = models.CharField(max_length=400, default='Mystery is in the air')
    profile_pic = models.URLField(max_length=45, blank=True, default='https://i.imgur.com/5jQrIYT.png', validators=[
        RegexValidator(
            regex='^(https://i.imgur.com/)\w{5,9}.\w{3,4}',
            message='Host your image on imgur.com !',
            code='invalid_profile_pic'
        ),
    ])


# This is to close the registrations !
class MyAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        return False
