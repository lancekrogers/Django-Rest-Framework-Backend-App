from .views import user_creation, genre_create_api, GenreDetail, MediaDetail, MediaCreate, render_comrades, \
    check_if_logged_in
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    url(r'^register/user/$', user_creation, name='register'),
    url(r'^genre/create/$', genre_create_api, name='genres'),
    url(r'^genre/detail/(?P<pk>[0-9]+)/$', GenreDetail.as_view()),
    url(r'^media/detail/(?P<pk>[0-9]+)/$', MediaDetail.as_view()),
    url(r'^media/list/create/$', MediaCreate.as_view()),
    url(r'^render/comrades/$', render_comrades),
    url(r'^logout/$',
        logout, {'next_page': 'preapplanding:landing'},
        name='Logout'),
    url(r'^check/login/$',
        check_if_logged_in,
        name='checklogin'),
]


urlpatterns = format_suffix_patterns(urlpatterns)


