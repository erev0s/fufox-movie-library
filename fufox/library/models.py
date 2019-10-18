import datetime
import json
from _decimal import Decimal
from users.models import CustomUser
from comment.models import Comment
from django.core import validators
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.conf import settings


class Genre(models.Model):
    name = models.CharField(max_length=27, help_text='Genre can be added here')
    prettyUrl = models.SlugField(max_length=100, validators=[validators.validate_slug])
    icon = models.URLField(default='', blank=True)

    def get_absolute_url(self):
        return reverse('genre-detail', kwargs={'pk': self.id, 'slug': self.prettyUrl})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            # create slug if the object is new
            self.prettyUrl = slugify(self.name)
        super(Genre, self).save(*args, **kwargs)


class Person(models.Model):
    name = models.CharField(max_length=30)
    capacity = models.CharField(max_length=50)
    prettyUrl = models.SlugField(max_length=100, validators=[validators.validate_slug])

    def get_absolute_url(self):
        return reverse('person-detail', kwargs={'pk': self.id, 'slug': self.prettyUrl})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:
            # create slug if the object is new
            self.prettyUrl = slugify(self.name)
        super(Person, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Person/People'


class Movie(models.Model):
    title = models.CharField(max_length=90)
    year = models.IntegerField(verbose_name='Year', blank=True, null=True)
    prettyUrl = models.SlugField(max_length=100)
    people = models.ManyToManyField(Person, help_text='Actors and Directors of the Movie')
    summary = models.TextField(max_length=400, help_text='Enter a brief description')
    genre = models.ManyToManyField(Genre, help_text='Select a genre')
    runtimes = models.IntegerField(verbose_name='Runtime', null=True, blank=True)
    score = models.DecimalField(blank=True, default=0.0, max_digits=2, decimal_places=1,
                                validators=[MinValueValidator(Decimal('0.01'))])
    poster = models.URLField(default='', blank=True)
    imdbid = models.CharField(unique=True, max_length=15)
    addedby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    addedwhen = models.DateTimeField(auto_now_add=True, blank=True)
    ratings = GenericRelation(Rating, related_query_name='user_rating')
    comments = GenericRelation(Comment)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse('movie-detail', args=[str(self.id)])
        return reverse('movie-detail', kwargs={'pk': self.id, 'slug': self.prettyUrl})

    class Meta:
        ordering = ['-addedwhen']
        permissions = (("can_add_movie", "Can actually add a movie to fufox"),
                       ("can_add_bulk", "Can add bulk from file"), )

    def save(self, *args, **kwargs):
        if not self.id:
            # create slug if the object is new
            self.prettyUrl = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def people_indexing(self):
        """People for indexing.
        Used in Elasticsearch indexing.
        """
        return [person.name for person in self.people.all()]

    @property
    def genres_indexing(self):
        """Genres for indexing.
        Used in Elasticsearch indexing.
        """
        return [genre.name for genre in self.genre.all()]


class Series(models.Model):
    title = models.CharField(max_length=90)
    year = models.CharField(max_length=30, verbose_name='Years')
    prettyUrl = models.SlugField(max_length=100)
    people = models.ManyToManyField(Person, help_text='actors and writers of the series')
    summary = models.TextField(max_length=400, help_text='Enter a brief description')
    genre = models.ManyToManyField(Genre, help_text='Select a genre')
    score = models.DecimalField(blank=True, default=0.0, max_digits=2, decimal_places=1,
                                validators=[MinValueValidator(Decimal('0.01'))])
    poster = models.URLField(default='', blank=True)
    imdbid = models.CharField(unique=True, max_length=15)
    addedby = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    addedwhen = models.DateTimeField(auto_now_add=True, blank=True)
    ratings = GenericRelation(Rating, related_query_name='user_rating')
    comments = GenericRelation(Comment)
    episodes = models.CharField(max_length=300, blank=True, null=True)

    def set_episodes(self, x):
        self.episodes = json.dumps(x)

    def get_episodes(self):
        return json.loads(self.episodes)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return reverse('movie-detail', args=[str(self.id)])
        return reverse('series-detail', kwargs={'pk': self.id, 'slug': self.prettyUrl})

    class Meta:
        ordering = ['-addedwhen']
        permissions = (("can_add_series", "Can actually add a series to fufox"),)

    def save(self, *args, **kwargs):
        if not self.id:
            # create slug if the object is new
            self.prettyUrl = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Series'
        verbose_name_plural = 'Series'

    @property
    def people_indexing(self):
        """People for indexing.
        Used in Elasticsearch indexing.
        """
        return [person.name for person in self.people.all()]

    @property
    def genres_indexing(self):
        """Genres for indexing.
        Used in Elasticsearch indexing.
        """
        return [genre.name for genre in self.genre.all()]


class Userchoices(models.Model):
    """
    I am not using generic Relation model here as we have the userchoices only for two models
    Adding the generic Relation would make things slower as it adds an extra layer -- more complicated
    A good tutorial if you would like to implement this part using generic relation is this on
    https://simpleisbetterthancomplex.com/tutorial/2016/10/13/how-to-use-generic-relations.html
    """
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movieobj = models.ForeignKey(Movie, on_delete=models.CASCADE, null=True)
    seriesobj = models.ForeignKey(Series, on_delete=models.CASCADE, null=True)
    haveyouseenit = models.BooleanField(default=False, null=True, blank=True)
    favorited = models.BooleanField(default=False, null=True, blank=True)
    incinema = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.username}|{self.movieobj.id}"

    class Meta:
        permissions = (("can_have_userchoices", "Can mark seen, favorite or at Cinema"),)
