from .views import user_creation, genre_create_api, GenreList, GenreDetail
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import login, authenticate



urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    url(r'^register-user/$', user_creation, name='register'),
    url(r'^genre-create/$', genre_create_api, name='genres'),
    url(r'^genre-get/$', GenreList.as_view(), name='genres_by_user'),
    url(r'^genre-detail/(?P<pk>[0-9]+)/$', GenreDetail.as_view()),
]


urlpatterns = format_suffix_patterns(urlpatterns)


