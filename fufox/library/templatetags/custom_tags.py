from django import template
from library.forms import SearchForm
from library.models import *

register = template.Library()


@register.filter
def howmanymovies(dummy):
    return Movie.objects.all().count()


@register.filter
def howmanydirectors(dummy):
    return Person.objects.filter(capacity='Director').count()


@register.filter
def howmanyactors(dummy):
    return Person.objects.filter(capacity='Actor').count()


@register.filter
def yourfavorites(you):
    return Userchoices.objects.filter(username=you, favorited=True).count()


@register.filter
def yourhaveseen(you):
    return Userchoices.objects.filter(username=you, haveyouseenit=True).count()


@register.filter
def yourcinemaones(you):
    return Userchoices.objects.filter(username=you, incinema=True).count()


@register.filter
def get_number_of_movies_for_person(person):
    mvs = Movie.objects.filter(people=person).count()
    srs = Series.objects.filter(people=person).count()
    return mvs + srs


@register.filter
def get_movie_name(movieid):
    return Movie.objects.filter(id=movieid).values('title')[0].get('title')

@register.filter
def create_movie_link(movieid):
    return 'movie/' + str(movieid) + '/'


@register.inclusion_tag('searchbar.html')
def navbar_search():
    return {'search_form': SearchForm()}
