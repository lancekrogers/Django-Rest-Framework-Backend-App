from .views import user_creation
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns
from django.contrib.auth import login, authenticate


urlpatterns = [
    url(r'^search/', include('haystack.urls')),
    url(r'^register-user/$', user_creation, name='register'),
]


urlpatterns = format_suffix_patterns(urlpatterns)


