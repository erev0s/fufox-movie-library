from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('profile/', profileview, name='profile_view'),
    path('profile/edit/', profileedit, name='profile_edit'),
]