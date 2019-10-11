from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from library.models import *
from django.views import generic
from django.shortcuts import get_object_or_404
from library.forms import *
from imdb import IMDb, IMDbError
from itertools import chain
from django.shortcuts import render
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search


def index(request):
    """View function for home page of site."""

    # How many movies do we have?
    num_movies = Movie.objects.all().count()

    # Lets get the latest 24 movies to show
    latestthirty = Movie.objects.order_by('-id')[:12]

    # Lets get also some genres to show
    genres = Genre.objects.order_by('id')

    # latest comments to a movie -- not replies to other comments
    latest_comments = Comment.objects.filter(parent=None).order_by('-id')[:5]

    # gets the latest favorites of me :D
    try:
        latest_suggestions = Movie.objects.filter(userchoices__favorited=True,
                                                  userchoices__username=CustomUser.objects.get(id=1)).order_by(
            '-addedwhen')[:5]
    except:
        latest_suggestions = None

    context = {
        'num_movies': num_movies,
        'last_thirty_movies': latestthirty,
        'genres': genres,
        'latest_comments': latest_comments,
        'suggestions': latest_suggestions,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class MovieListView(generic.ListView):
    model = Movie
    paginate_by = 13
    queryset = Movie.objects.order_by('-addedwhen')
    template_name = 'library/movie_list.html'  # not needed but for clarity

    def get_context_data(self, *, object_list=None, **kwargs):
        # Call the base implementation first to get the context
        context = super(MovieListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['howManyGenres'] = Genre.objects.all().count()
        return context


class SeriesListView(generic.ListView):
    model = Series
    paginate_by = 13
    queryset = Series.objects.order_by('-addedwhen')
    template_name = 'library/series-list.html'  # not needed but for clarity

    def get_context_data(self, *, object_list=None, **kwargs):
        # Call the base implementation first to get the context
        context = super(SeriesListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['howManyGenres'] = Genre.objects.all().count()
        return context


def MovieDetailView(request, pk, slug):
    if request.method == 'GET':
        # Get the movie object and pass it to the context
        movieobj = get_object_or_404(Movie, id=pk)
        people = Person.objects.filter(movie=movieobj)
        directors = people.filter(capacity='Director')
        actors = people.filter(capacity='Actor')
        context = {
            'movie': movieobj,
            'directors': directors,
            'actors': actors,
        }
        if request.user.is_authenticated:
            # get all that is needed for authenticated users
            check, created = Userchoices.objects.get_or_create(username=request.user, movieobj=movieobj)
            context['seen'] = check.haveyouseenit
            context['fav'] = check.favorited
            context['incinema'] = check.incinema

        return render(request, 'library/movie_detail.html', context=context)


def SeriesDetailView(request, pk, slug):
    if request.method == 'GET':
        # Get the movie object and pass it to the context
        seriesobj = get_object_or_404(Series, id=pk)
        people = Person.objects.filter(series=seriesobj)
        writer = people.filter(capacity='Writer')
        actors = people.filter(capacity='Actor')
        seasons = seriesobj.get_episodes()
        context = {
            'movie': seriesobj,
            'writers': writer,
            'actors': actors,
            'seasons': seasons,
        }
        if request.user.is_authenticated:
            # get all that is needed for authenticated users
            check, created = Userchoices.objects.get_or_create(username=request.user, seriesobj=seriesobj)
            context['seen'] = check.haveyouseenit
            context['fav'] = check.favorited
            context['incinema'] = check.incinema

        return render(request, 'library/series_detail.html', context=context)


class PersonListView(generic.ListView):
    model = Person
    # paginate_by = 20
    queryset = Person.objects.order_by('name')
    template_name = 'library/person_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        # Call the base implementation first to get the context
        context = super(PersonListView, self).get_context_data(**kwargs)

        context['numActors'] = Person.objects.filter(capacity='Actor').count()
        context['numDirectors'] = Person.objects.filter(capacity='Director').count()
        context['numWriters'] = Person.objects.filter(capacity='Writer').count()
        return context


def PersonDetailView(request, pk, slug):
    if request.method == "GET":
        person = get_object_or_404(Person, pk=pk)
        alllist = list(chain(person.movie_set.all(), person.series_set.all()))
        context = {
            'person': person,
            'alllist': alllist,
        }

        return render(request, 'library/person_detail.html', context=context)


def GenreDetailView(request, pk, slug):
    if request.method == "GET":
        genre = get_object_or_404(Genre, pk=pk)
        alllist = list(chain(genre.movie_set.all(), genre.series_set.all()))
        context = {
            'genre': genre,
            'alllist': alllist,
        }

        return render(request, 'library/genre_detail.html', context=context)


@permission_required('library.can_have_userchoices')
def Adduserchoices(request, id):
    if request.method == 'POST':
        if request.POST.get('type') == 'movie':
            movieobj = get_object_or_404(Movie, id=id)
            check = get_object_or_404(Userchoices, username=request.user, movieobj=movieobj)
        elif request.POST.get('type') == 'series':
            movieobj = get_object_or_404(Series, id=id)
            check = get_object_or_404(Userchoices, username=request.user, seriesobj=movieobj)
        else:
            return HttpResponse("Not a movie or a Series Object")
        if request.POST.get('choice') == 'seen':
            check.haveyouseenit = not check.haveyouseenit
        elif request.POST.get('choice') == 'fav':
            check.favorited = not check.favorited
        elif request.POST.get('choice') == 'cinema':
            check.incinema = not check.incinema
        else:
            return HttpResponse("Are you sure you didnt mess things up??")
        check.save()
        return HttpResponse("1")


def Addmovie(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = AddMovieIMDBForm(request.POST)
            if form.is_valid():
                imdbid = form.cleaned_data["movienumber"]
                ia = IMDb()
                try:
                    movie = ia.get_movie(imdbid)
                except IMDbError as e:
                    print(e)
                    return HttpResponse("0")

                #  Check if it is a movie or a tv series
                if movie['kind'] == 'movie':
                    mv = True
                    # Lets see if the movie already exists
                    check, created = Movie.objects.get_or_create(imdbid=str(imdbid), title=movie.get('long imdb title'))
                elif 'series' in movie['kind']:
                    mv = False
                    check, created = Series.objects.get_or_create(imdbid=str(imdbid),
                                                                  title=movie.get('long imdb title'))
                else:
                    return HttpResponse("0")

                # if it already exists
                if not created:
                    return redirect('movie-detail', pk=check.id)
                check.title = movie.get('long imdb title')
                if mv:
                    check.year = movie.get('year')
                    for director in movie.get('directors'):
                        checkdirector, created = Person.objects.get_or_create(name=director, capacity='Director')
                        check.people.add(checkdirector)
                else:
                    check.year = movie.get('series years')
                    for writer in movie.get('writer'):
                        checkwriter, created = Person.objects.get_or_create(name=writer, capacity='Writer')
                        check.people.add(checkwriter)
                for actor in movie.get('cast')[:3]:
                    checkactor, created = Person.objects.get_or_create(name=actor, capacity='Actor')
                    check.people.add(checkactor)
                plot = movie.get('plot')[0]
                ploc = plot.split("::")
                check.summary = ploc[0]
                for genre in movie.get('genres')[:3]:
                    checkgenre, created = Genre.objects.get_or_create(name=genre)
                    check.genre.add(checkgenre)
                check.score = movie.get('rating')
                check.poster = movie.get('full-size cover url')
                check.addedby = request.user
                if not mv:
                    ep = {}
                    print(" Seasons = " + str(movie.get('seasons')))
                    ia.update(movie, "episodes")
                    for i in range(1, movie.get('seasons') + 1):
                        ep[i] = len(movie.get('episodes')[i])
                    check.set_episodes(ep)
                check.save()

                # lets also save in a text file which movie/series that was
                with open("incoming.txt", "a+") as text_file:
                    print(f"{imdbid}\nTitle: {movie.get('long imdb title')}", file=text_file)

                if mv:
                    return HttpResponseRedirect(reverse('movies'))
                else:
                    return HttpResponseRedirect(reverse('series'))
            else:
                return render(request, 'library/add_movie_form.html', {'form': form})
        else:
            return HttpResponse("2")
    context = {
        'form': AddMovieIMDBForm(),
    }

    return render(request, 'library/add_movie_form.html', context=context)


@staff_member_required
def Addbulkmovies(request):
    if request.method == 'POST':
        if request.user.is_superuser:
            f = open('movies.txt')
            for line in f:
                if len(line) > 10:
                    print(line)
                    continue
                ia = IMDb()
                try:
                    movie = ia.get_movie(line)
                except IMDbError as e:
                    print(e)
                    continue
                if movie['kind'] == 'movie':
                    mv = True
                    # Lets see if the movie already exists
                    check, created = Movie.objects.get_or_create(imdbid=str(line), title=movie.get('long imdb title'))
                elif 'series' in movie['kind']:
                    mv = False
                    check, created = Series.objects.get_or_create(imdbid=str(line), title=movie.get('long imdb title'))
                else:
                    print("Not a movie or a Series .... weird... it returned as movie['kind']----> " + movie['kind'])
                    continue

                # if it already exists
                if not created:
                    print(check.title + " already exists in our Database :D")
                    continue
                check.title = movie.get('long imdb title')
                if mv:
                    check.year = movie.get('year')
                    for director in movie.get('directors'):
                        checkdirector, created = Person.objects.get_or_create(name=director, capacity='Director')
                        check.people.add(checkdirector)
                else:
                    check.year = movie.get('series years')
                    for writer in movie.get('writer'):
                        checkwriter, created = Person.objects.get_or_create(name=writer, capacity='Writer')
                        check.people.add(checkwriter)
                for actor in movie.get('cast')[:3]:
                    checkactor, created = Person.objects.get_or_create(name=actor, capacity='Actor')
                    check.people.add(checkactor)
                plot = movie.get('plot')[0]
                ploc = plot.split("::")
                check.summary = ploc[0]
                for genre in movie.get('genres')[:3]:
                    checkgenre, created = Genre.objects.get_or_create(name=genre)
                    check.genre.add(checkgenre)
                check.score = movie.get('rating')
                check.poster = movie.get('full-size cover url')
                check.addedby = request.user
                if not mv:
                    ep = {}
                    for i in range(1, movie.get('seasons') + 1):
                        ep[i] = len(movie.get('episodes')[i])
                    check.set_episodes(ep)
                check.save()
            f.close()
            return HttpResponseRedirect(reverse('movies'))


def search_results(request):
    """
    It is the general search, it searches over the indexes of the movies and the series
    this is the reason i am using the Search() instead of directly the document
    """
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = SearchForm(request.POST)
            if form.is_valid():
                search_in_title = form.cleaned_data["searchintitle"]
                # s = Search(using=Elasticsearch('localhost'))
                client = Elasticsearch('elasticsearch:9200')

                sreq = Search().using(client).query("multi_match", query=search_in_title, fields=['title', 'summary'])

                # TODO the line below provides the suggestions -- use it
                # sreq = sreq.suggest('title_suggestions', search_in_title, completion={'field': 'title.suggest'})
                response = sreq.execute()
                # print(response.to_dict())

                total_hits = response.hits.total
                time_took = response.took  # time in milliseconds

                context = {
                    'term': search_in_title,
                    'total_hits': total_hits,
                    'time_took': time_took,
                    'hits': response.hits,  # https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
                    # #pagination
                    'form': form,
                    # 'title_suggestions': ssug,
                }

                return render(request, 'library/search_results.html', context=context)
            else:
                context = {
                    'form': form,
                }

                return render(request, 'library/search_results.html', context=context)
        else:
            return redirect('account_login')
    elif request.method == 'GET':
        return render(request, 'library/search_results.html', {})


def custom_search(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CustomSearch(request.POST)
            if form.is_valid():
                title = form.cleaned_data["title"]
                summary = form.cleaned_data["summary"]
                genre = form.cleaned_data["genre"]
                person = form.cleaned_data["person"]
                yearfrom = form.cleaned_data["yearfrom"]
                yearto = form.cleaned_data["yearto"]
                scorefrom = form.cleaned_data["scorefrom"]
                scoreto = form.cleaned_data["scoreto"]
                typeof = form.cleaned_data["typeof"]

                client = Elasticsearch('elasticsearch:9200')
                if int(typeof) == 1:
                    s = Search(using=client, index="s_movies")
                else:
                    s = Search(using=client, index="s_series")

                if title:
                    s = s.query("match", title=title)

                if summary:
                    s = s.query("match", summary=summary)

                if person:
                    s = s.query("match", people=person)

                if genre:
                    s = s.query("match", genres=genre)

                if scorefrom and scoreto:
                    s = s.query('range', score={'gte': scorefrom, 'lte': scoreto})
                if scorefrom and not scoreto:
                    s = s.query('range', score={'gte': scorefrom})
                if not scorefrom and scoreto:
                    s = s.query('range', score={'lte': scoreto})

                if int(typeof) == 1:
                    if yearfrom and yearto:
                        s = s.query('range', year={'gte': yearfrom, 'lte': yearto})
                    if yearfrom and not yearto:
                        s = s.query('range', year={'gte': yearfrom})
                    if not yearfrom and yearto:
                        s = s.query('range', year={'lte': yearto})

                response = s.execute()
                total_hits = response.hits.total
                time_took = response.took  # time in milliseconds

                # In order to know in the template if to link to movies or to series
                # we pass in the context the mos(movie or series)
                if int(typeof) == 1:
                    mos = 'movie'
                else:
                    mos = 'series'

                context = {
                    'form': form,
                    'total_hits': total_hits,
                    'time_took': time_took,
                    'hits': response.hits,
                    'type': mos,
                }

                return render(request, 'library/custom_search.html', context=context)
            else:
                context = {
                    'form': form,
                }

                return render(request, 'library/custom_search.html', context=context)
        else:
            return redirect('account_login')
    elif request.method == 'GET':
        context = {
            'form': CustomSearch()
        }
        return render(request, 'library/custom_search.html', context=context)
