from django import forms
import re
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

class AddMovieIMDBForm(forms.Form):
    movienumber = forms.CharField(max_length=100, help_text="Enter the IMDb url.")

    def clean_movienumber(self):
        data = self.cleaned_data['movienumber']
        if ((len(data) < 6) or (len(data) > 11)) and not data.isdigit():
            # then this is not only the imdb id, we need to attempt to extract it
            try:
                maybetheid = re.search("(?<=imdb.com/title/tt)[^\/]{4,10}", str(data), flags=0).group()
            except:
                raise forms.ValidationError('IMDb id does not seem correct')
            if not maybetheid.isdigit():
                raise forms.ValidationError('IMDb id does not seem correct')
            else:
                return maybetheid
        else:
            return data


class SearchForm(forms.Form):
    searchintitle = forms.CharField(max_length=100, label='',
                                    widget=forms.TextInput(attrs={'placeholder': 'search...'}))


CHOICES = (
    (1, 'Movies'),
    (0, 'Series')
)

class CustomSearch(forms.Form):
    title = forms.CharField(required=False, max_length=100, label='',
                            widget=forms.TextInput(attrs={'placeholder': 'in title...'}))
    summary = forms.CharField(required=False, max_length=100, label='',
                              widget=forms.TextInput(attrs={'placeholder': 'in summary...'}))

    genre = forms.CharField(required=False, max_length=100, label='',
                            widget=forms.TextInput(attrs={'placeholder': 'is included in genres...'}))

    person = forms.CharField(required=False, max_length=100, label='',
                             widget=forms.TextInput(attrs={'placeholder': 'this person is part of it...'}))

    yearfrom = forms.IntegerField(required=False, label='From Year',)
    yearto = forms.IntegerField(required=False, label='To Year',)
    scorefrom = forms.FloatField(required=False, label='From Score',)
    scoreto = forms.FloatField(required=False, label='To Score',)
    typeof = forms.ChoiceField(required=True, label='', choices=CHOICES,
                               widget=forms.RadioSelect(attrs={'class': 'Radio'}),
                               initial=1)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        summary = cleaned_data.get("summary")
        genre = cleaned_data.get("genre")
        person = cleaned_data.get("person")
        yearfrom = cleaned_data.get("yearfrom")
        yearto = cleaned_data.get("yearto")
        scorefrom = cleaned_data.get("scorefrom")
        scoreto = cleaned_data.get("scoreto")
        if not (title or summary or genre or person or yearfrom or yearto or scorefrom or scoreto):
            raise forms.ValidationError(
                "You need to provide at least 1 value in a field")

    # MAYBE not the best option but i wanted to try it out !
    # it was made according to
    #  https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('title', css_class='form-group col-md-6 mb-0'),
                Column('summary', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('genre', css_class='form-group col-md-6 mb-0'),
                Column('person', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('yearfrom', css_class='form-group col-md-3 mb-0'),
                Column('yearto', css_class='form-group col-md-3 mb-0'),
                Column('scorefrom', css_class='form-group col-md-3 mb-0'),
                Column('scoreto', css_class='form-group col-md-3 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('typeof', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Submit('submit', 'Search', css_class='')
        )

