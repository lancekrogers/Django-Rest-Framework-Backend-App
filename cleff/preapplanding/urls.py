from django.conf.urls import include, url
from .views import landing, test

urlpatterns = [
    url(r'^$', landing, name='landing'),
    url(r'^test/$', test, name='test')
]