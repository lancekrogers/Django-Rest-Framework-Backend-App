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
        use_r = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        use_r.set_password(validated_data['password'])
        use_r.save()
        Musician.objects.create(user=use_r, email=validated_data['email'], is_musician=True)
        return use_r


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


class MusicianProfileUpdateSerializer(serializers.ModelSerializer):
    genres = serializers.StringRelatedField(many=True)
    instruments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Musician
        fields = ('profile_image',
                  'summary',
                  'genres',
                  'instruments',
                  'company', )


class MusianUpdateSearchRangeSerializer(serializers.ModelSerializer):

    class Meta:
        models = Musician
        fields = ('search_range',)

class MusicianUpdateFriendsSerializer(serializers.ModelSerializer):
    friends = serializers.StringRelatedField(many=True)

    class Meta:
        models = Musician
        fields = ('friends',)


class MusicianMediaSerializer(serializers.ModelSerializer):
    media = serializers.StringRelatedField(many=True)

    class Meta:
        models = Musician
        fields = ('media',)
