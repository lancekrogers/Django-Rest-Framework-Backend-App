from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Musician, Genre, Media, Instrument
from .choices_list import GENRES

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('genre', 'description')


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ('title', 'audio')

class InstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = ('name', 'description')


