# Fufox Movie Library
![Fufox Movie Library](https://i.imgur.com/qDUkNPH.png "Fufox Movie Library")

FuFox is a relatively light weight movie and TV series library created with Django. It can be used to keep track of movies and TV series you have watched and also rate them and suggest them to friends. It started as a project so I can get more familiar with Django and play around with Postgresql and Elasticsearch. I was skeptical about Elasticsearch in the beginning as it requires some resources in order to run properly but it offers really nice features which I wanted to explore.   
The code is by no means ready for production but it serves my purposes for creating a library to keep track of my movies and shows. I will update it whenever possible with features I am adding as time passes!  


<img src="/fufox_preview.gif?raw=true">


## Bring Up FuFox
The project is deployed using `docker-compose`. This allows everything to be set up with minimal effort for anyone who might want to use it.
To bring it up simply run:
~~~~
docker-compose up --build
~~~~

This will bring up the FuFox library along with Postgresql for its database, Elasticsearch to support searching and Nginx to serve the content. Gunicorn is used to run FuFox.

A default admin user is being created upon bringing up the project with details
`username:erev0s`, `email:admin@example.com`, `password:djangoproject`


## Main Features
Following is a list of features that have been added to FuFox.
 - Support to add Movies|Series|Genres|Actors|Directors|Writers
 - Automatic fetch of movie/series details through IMDb (using [IMDbPy](https://github.com/alberanid/imdbpy))
 - Mark movies/series if you have seen them, if they belong to the favorite ones and if you have seen it in cinema.
 - User rating system for movies/series (based on [django-star-rating](https://github.com/wildfish/django-star-ratings))
 - Custom User Model with register/login/profile and more pages
 - Well defined user permissions
 - Support for registration through Social Pages (Facebook, Twitter etc), using [django-allauth](https://github.com/pennersr/django-allauth)
 - Ajax based commenting system for movies/series based on [Comment](https://github.com/Radi85/Comment) with support for markdown
 - General searching and more precise searching through Elasticsearch.
 - Dynamic listing/filtering in multiple locations
 - Bootstrap/Font-Awesome for responsiveness
 - SEO friendly structure.
 - more...



## FAQ
How can I rebuild the indexes of the Elasticsearch? |
--- |
Simply run `docker exec -it fufox python manage.py search_index --rebuild` and answer `Y` when asked |

How can I add movies/series in bulk? |
--- |
Inside the folder fufox you will find a text file names `movies.txt`. You can fill in there the IMDb urls of the movies/series you would like to add and visit the Admin Dashboard. In `Library` you will find a button named `Bulk Import Movies`. |


## To be done
Let me know of suggestions or questions!


## Changelog

 - 10/2019
   - Relaxed regex so users can add movies/series using mobile links of IMDb
   - Fixed permission on bulk adding movies/series
   - Minor change in structure of index.html
   - Fix duplicate submission issue
   - Added run time in movies
