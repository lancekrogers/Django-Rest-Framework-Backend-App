from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Musician, Genre, Media, Instrument
from .choices_list import GENRES


# register
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class GenreSerializer(serializers.ModelSerializer):
    genre = serializers.ChoiceField(choices=GENRES)

    class Meta:
        model = Genre
        fields = ('user_pk', 'genre', 'description')


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Media
        fields = ('user_pk', 'title', 'audio')


class InstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = ('user_pk', 'name', 'description')


