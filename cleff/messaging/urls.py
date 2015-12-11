from .views import message_create
from django.conf.urls import include, url
from rest_framework.urlpatterns import format_suffix_patterns




urlpatterns = [
    url(r'^create/',
        message_create),

]

urlpatterns = format_suffix_patterns(urlpatterns)