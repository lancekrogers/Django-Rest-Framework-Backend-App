from .views import user_creation, genre_create_api, get_genres_by_user
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import login, authenticate



urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    url(r'^register-user/$', user_creation, name='register'),
    url(r'^genre-create/$', genre_create_api, name='genres'),
    url(r'^genre-get/(?P<pk>\d+)/$', get_genres_by_user, name='genres_by_user'),
]


urlpatterns = format_suffix_patterns(urlpatterns)


