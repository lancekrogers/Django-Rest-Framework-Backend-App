import datetime
from haystack import indexes
from .models import Musician, Location
from haystack.utils.geo import Point
from django.contrib.gis.geos import GEOSGeometry


class LocationIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True,
                             use_template=True,)
    location = indexes.LocationField(model_attr='get_location')

    def get_model(self):
        return Musician
