import json
from .choices_list import GENRES
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image  # this is needed for the models.ImageField to work
from geoposition.fields import GeopositionField
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
from django.utils.translation import ugettext_lazy as _
import random
# Create your models here.

class MaxOrMinIntegerField(models.IntegerField):
    description = _("Positive integer")

    def get_internal_type(self):
        return "PositiveIntegerField"

    def formfield(self, **kwargs):
        defaults = {'min_value': 0, 'max_value': 24901}
        defaults.update(kwargs)
        return super(MaxOrMinIntegerField, self).formfield(**defaults)


# An Abstract Base User Model
class ProfileModel(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    email = models.EmailField(blank=True, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    profile_image = models.ImageField(upload_to='profile_image/%Y/%m/%d/', blank=True)
    locations = models.ManyToManyField('Location', blank=True)
    current_location = GeopositionField(blank=True)  # comrades are the matched users
    is_musician = models.BooleanField(default=False)  # the more times a comrade with the same user_pk
    search_range = MaxOrMinIntegerField(default=30)  #
    comrades = models.ManyToManyField('Comrade', blank=True)  #

    def profile_image_func(self):
        if self.profile_image.url:
            return self.profile_image.url
        else:
            pass

    def get_location(self):
        # Remember, longitude FIRST in Geo Django!
        try:
            lat = float(self.current_location.latitude)
            lon = float(self.current_location.longitude)
            return Point(lon, lat)
        except:
            # coordinates for Antartica
            lat = 90.0000
            lon = 0.0000
            return Point(lon, lat)

    class Meta:
        abstract = True

# The main user profile model
class Musician(ProfileModel):
    genres = models.ManyToManyField('Genre', blank=True)
    summary = models.TextField(blank=True)
    company = models.CharField(max_length=60, blank=True)
    media = models.ManyToManyField('Media', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    instruments = models.ManyToManyField('Instrument', blank=True)
    friends = models.ManyToManyField('SavedMusician', blank=True)

    def __str__(self):
        return '{}'.format(self.user.username)


class Genre(models.Model):
    genre = models.CharField(choices=GENRES, max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return '{}'.format(self.genre)

    class Meta:
        ordering = ['timestamp']


class Media(models.Model):
    user_pk = models.IntegerField(default=-1)
    title = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)
    youtube_code = models.CharField(max_length=20, blank=True)
    audio = models.FileField(upload_to='audio/%Y/%m/%d/{}'.format('sound'), blank=True)

    def __str__(self):
        return '{} {}'.format(self.title, self.timestamp)

    class Meta:
        ordering = ['-timestamp']


class Instrument(models.Model):
    rank = models.FloatField(default=0)
    numerator = models.IntegerField(default=0)
    denominator = models.IntegerField(default=1)
    name = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        ordering = ['-rank']


class Location(models.Model):
    user_pk = models.IntegerField(default=-1)
    location = GeopositionField(blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return '{}'.format(self.description)

    def get_location(self):
        # Remember, longitude FIRST in Geo Django!
        lat = float(self.location.latitude)
        lon = float(self.location.longitude)
        return Point(lon, lat)


@receiver(post_save, sender=Location)
def set_description(sender, instance, created=False, **kwargs):
    if created:
        try:
            geolocator = Nominatim()
            lat = instance.location.latitude
            lon = instance.location.longitude
            print('.....{}, {}........'.format(lat, lon))
            loc = geolocator.reverse([lat, lon])
            address = loc.address
            print(address)
            instance.description = address
            instance.save()
        except:
            try:
                geolocator = Nominatim()
                lat = instance.location.latitude
                lon = instance.location.longitude
                print('..........{}, {}........'.format(lat, lon))
                loc = geolocator.reverse([lat, lon])
                address = loc.address
                print(address)
                instance.description = address
                instance.save()
            except:
                print('......location post save didnt work.......')
                instance.description = 'Location created on {}'.format(instance.timestamp)
                instance.save()
                pass


class SavedMusician(models.Model):
    numbre = models.IntegerField()
    saver_musician = models.ForeignKey(Musician, blank=True, null=True)
    date_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "{}".format(Musician.objects.get(pk=self.numbre))


class Comrade(models.Model):
    numbre = models.OneToOneField(SavedMusician, blank=True, primary_key=True)
    date_stamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return 'Comrade {}'.format(Musician.objects.get(pk=self.numbre.numbre))

    class Meta:
        ordering = ['-date_stamp']