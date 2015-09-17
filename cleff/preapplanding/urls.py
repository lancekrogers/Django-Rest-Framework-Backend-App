from django.conf.urls import include, url
from .views import landing

urlpatterns = [
    url(r'^$', landing, name='landing')
]