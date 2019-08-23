from django.contrib import admin
from library.models import *


class PersonAdmin(admin.ModelAdmin):
    pass


class MovieAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('people',)
    fields = ['poster', ('title', 'prettyUrl'), ('genre', 'score'), 'people', 'summary', 'imdbid']


admin.site.register(Person, PersonAdmin)
admin.site.register(Genre)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Series)
