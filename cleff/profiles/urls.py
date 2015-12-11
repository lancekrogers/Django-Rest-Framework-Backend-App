from .views import user_creation, MediaDetail, MediaListCreate, render_comrades, \
    check_if_logged_in, genre_choices, genre_add_delete_api, instrument_choices, \
    instrument_add_delete_api, login_account, logout_account
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth.views import logout

urlpatterns = [
    url(r'^search/',
        include('haystack.urls')),
    url(r'^register/user/$',
        user_creation,
        name='register'),
    url(r'^genre/add-or-delete/$',
        genre_add_delete_api,
        name='genres'),
    url(r'^genre/choices/$',
        genre_choices),
    url(r'^media/detail/(?P<pk>[0-9]+)/$',
        MediaDetail.as_view()),
    url(r'^media/list/create/$',
        MediaListCreate.as_view()),
    url(r'^render/comrades/$',
        render_comrades),
    url(r'^logout/$',
        logout_account, # {'next_page': 'preapplanding:landing'},
        name='Logout'),
    url(r'^check/login/$',
        check_if_logged_in,
        name='checklogin'),
    url(r'^instrument/choices/$',
        instrument_choices),
    url(r'^instrument/add-or-delete/$',
        instrument_add_delete_api),
    url(r'^login/$',
        login_account),
]


urlpatterns = format_suffix_patterns(urlpatterns)


