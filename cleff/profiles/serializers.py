from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import serializers
from .models import Musician, Genre, Media, Instrument
from .choices_list import GENRES

# register
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            use_r = User(
                email=validated_data['email'],
                username=validated_data['username']
            )
            use_r.set_password(validated_data['password'])
            use_r.save()
            Musician.objects.create(user=use_r, email=validated_data['email'], is_musician=True)
        except IntegrityError:
            pass
        return use_r


class GenreSerializer(serializers.ModelSerializer):
    genre = serializers.ChoiceField(choices=GENRES)

    class Meta:
        model = Genre
        fields = ('genre',)


class MediaSerializer(serializers.ModelSerializer):
    audio = serializers.FileField(required=True)
    user_pk = serializers.IntegerField(required=True)

    class Meta:
        model = Media
        fields = ('user_pk', 'title', 'audio')


class InstrumentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Instrument
        fields = ('name', )


class MusicianProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Musician
        fields = ('profile_image',
                  'summary',
                  'company', )


class MusianUpdateSearchRangeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Musician
        fields = ('search_range',)




