from django.urls import path, re_path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.index, name='index'),
    path('movies/', views.MovieListView.as_view(), name='movies'),
    path('series/', views.SeriesListView.as_view(), name='series'),
    re_path(r'^movie/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))?/$', views.MovieDetailView, name='movie-detail'),
    re_path(r'^series/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))?/$', views.SeriesDetailView, name='series-detail'),
    path('person/', views.PersonListView.as_view(), name='people'),
    re_path(r'^person/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))?/$', views.PersonDetailView, name='person-detail'),
    re_path(r'^genre/(?P<pk>\d+)(?:/(?P<slug>[\w\d-]+))?/$', views.GenreDetailView, name='genre-detail'),
    re_path(r'^add-to/(?P<id>.*)', views.Adduserchoices, name='add_to_userchoices'),
    path('movie/add/', views.Addmovie, name='add-movie-form'),
    path('movie/bulk-add/', views.Addbulkmovies, name='add-bulk-movies'),
    re_path(r'^ratings/', include('star_ratings.urls', namespace='ratings')),
    path('comment/', include('comment.urls')),
    path('api/', include('comment.api.urls')),  # for API Framework
    # path('search/', include(router.urls)),
    re_path(r'^search-results', views.search_results, name='search_results'),
    re_path(r'custom-search', views.custom_search, name='custom_search')
]


# Admin Site Config
admin.sites.AdminSite.site_header = 'FuFox Admin'
admin.sites.AdminSite.site_title = 'FuFox Admin Dashboard'
admin.sites.AdminSite.index_title = 'FuFox Admin Dashboard'