from .views import update_comrades_view
from django.conf.urls import url

urlpatterns = [
    url(r'^$', update_comrades_view, name='update_comrades'),
]