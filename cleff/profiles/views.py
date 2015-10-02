from .models import Genre
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import UserSerializer, GenreSerializer
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core import serializers as serial2
from rest_framework.views import APIView
from rest_framework import authentication, permissions

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


def get_genres_by_user(request, pk):
    this = pk
    if request.method == 'GET':
        genres = Genre.objects.filter(user_pk=this)
        for genre in genres:
            return JsonResponse(genres, safe=False)
    else:
        return HttpResponse('NOT ALLOWED')


