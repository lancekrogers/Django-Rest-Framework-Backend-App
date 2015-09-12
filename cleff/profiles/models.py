from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image  # this is needed for the models.ImageField to work
from geoposition.fields import GeopositionField
from geopy.geocoders import Nominatim
from django.contrib.gis.geos import Point
# Create your models here.


class ProfileModel(models.Model):
    user = models.OneToOneField(User, primary_key=True)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=15, blank=True)
    last_name = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profile_image/%Y/%m/%d', blank=True)
    locations = models.ManyToManyField('Location', blank=True)
    current_location = GeopositionField(blank=True)  # comrades are the matched users
    is_musician = models.BooleanField(default=False)  # the more times a comrade with the same user_pk
    search_range = models.IntegerField(default=50)  #
    comrades = models.ManyToManyField('Comrade', blank=True)  #

    def profile_image_func(self):
        if self.profile_image.url:
            return self.profile_image.url
        else:
            pass

    class Meta:
        abstract = True


class Musician(ProfileModel):
    genres = models.ManyToManyField('Genre', blank=True)
    summary = models.TextField(blank=True)
    company = models.CharField(max_length=60, blank=True)
    media = models.ManyToManyField('Media', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    instruments = models.ManyToManyField('Instrument', blank=True)
    friends = models.ManyToManyField('SavedMusician', blank=True)

    def __str__(self):
        return '{}'.format(self.user.username)

    def latest_video(self):
        if Media.objects.filter(user_pk=self.pk):
            return Media.objects.filter(user_pk=self.pk)[0]


class Genre(models.Model):
    user_pk = models.IntegerField(default=-1)
    genre = models.CharField(max_length=20)
    description = models.CharField(max_length=140, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.genre, self.description)


class Media(models.Model):
    user_pk = models.IntegerField(default=-1)
    title = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    youtube_code = models.CharField(max_length=20, blank=True)
    video = models.FileField(upload_to='video/%Y/%m/%d/{}'.format('video'), blank=True)
    audio = models.FileField(upload_to='audio/%Y/%m/%d/{}'.format('sound'), blank=True)
    genre = models.ManyToManyField('Genre', blank=True)

    def __str__(self):
        return '{} {}'.format(self.title, self.timestamp)

    class Meta:
        ordering = ['-timestamp']


class Instrument(models.Model):
    user_pk = models.IntegerField(default=-1)
    family = models.CharField(max_length=60)
    description = models.CharField(max_length=50, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.family, self.description)


class Location(models.Model):
    user_pk = models.IntegerField(default=-1)
    location = GeopositionField(blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return '{}'.format(self.description)

    def get_location(self):
        # Remember, longitude FIRST!
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
                print('......didnt work.......')
                instance.description = 'Location created on {}'.format(instance.date_added)
                instance.save()
                pass


class SavedMusician(models.Model):
    numbre = models.IntegerField()
    saver_musician = models.ForeignKey(Musician, blank=True, null=True)
    date_stamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return "{}".format(Musician.objects.get(pk=self.numbre))


class Comrade(models.Model):
    numbre = models.OneToOneField(SavedMusician, blank=True, primary_key=True)
    date_stamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return 'Comrade {}'.format(Musician.objects.get(pk=self.numbre.numbre))

    class Meta:
        ordering = ['-date_stamp']