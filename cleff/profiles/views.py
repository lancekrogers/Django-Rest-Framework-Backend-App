from .models import Genre, Media
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, GenreSerializer, MediaSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers as serial2
from rest_framework.views import APIView
from rest_framework import authentication, permissions, generics

# Create your views here.


@csrf_exempt
@api_view(['POST'])
def user_creation(request):
    # this is a temporary api view for creating users
    # this view will be used until token authentication is in place
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # print(request.data['email'])
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('NOT ALLOWED', status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
def genre_create_api(request):
    # an api view for the genre model
    # authentication will be added later alon with all other views
    if request.method == 'POST':
        serializer = GenreSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('NOT ALLOWED', status=status.HTTP_400_BAD_REQUEST)


class GenreDetail(APIView):
    """

    retrieve update or delete a genre

    """

    def get_object(self, pk):
        try:
            return Genre.objects.get(pk=pk)
        except Genre.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        genre = self.get_object(pk)
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        genre = self.get_object(pk)
        serializer = GenreSerializer(genre, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        genre = self.get_object(pk)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MediaDetail(APIView):

    def get_object(self, pk):
        try:
            return Media.objects.get(pk=pk)
        except Media.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        media = self.get_object(pk)
        serializer = MediaSerializer(media)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        media = self.get_object(pk)
        serializer = MediaSerializer(media, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        media = self.get_object(pk)
        media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MediaCreate(generics.ListCreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

