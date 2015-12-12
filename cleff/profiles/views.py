from cleff.settings import STATIC_URL
from .choices_list import GENRES, INSTRUMENT_CLASSES
from .ranking import update_instrument_rank
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Genre, Media, Musician, Instrument
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from .serializers import UserSerializer, GenreSerializer, MediaSerializer
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes, authentication_classes
from rest_framework.response import Response
from django.core import serializers as django_serializers
from rest_framework.views import APIView
from rest_framework import authentication, permissions, generics, viewsets
import random


# Create your views here.
@renderer_classes((JSONRenderer,))
@api_view(['POST'])
def user_creation(request):
    """
        This function creates a user and logs them in returning a HTTP 200 OK Response
        with logged in: True.  To authenticate further use basic authentication.  Look
        in the music network new folder in your browser for instructions to do this with
        ajax.
    """
    # this is a temporary api view for creating users
    # this view will be used until token authentication is in place
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                username = request.data['username']
                password = request.data['password']
                user = authenticate(username=username, password=password)
                login(request, user)
                data = {'data': serializer.data, 'logged in': True}
                return JsonResponse(data=data, status=status.HTTP_201_CREATED)
                #return redirect('profiles:checklogin')
            except:
                pass
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response('NOT ALLOWED', status=status.HTTP_400_BAD_REQUEST)
'''
@api_view(['POST'])
def user_creation(request):
    """
        This function creates a user and logs them in returning a HTTP 200 OK Response
        with logged in: True.  To authenticate further use basic authentication.  Look
        in the music network new folder in your browser for instructions to do this with
        ajax.
    """
    # this is a temporary api view for creating users
    # this view will be used until token authentication is in place
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            try:
                username = request.data['username']
                password = request.data['password']
                user = authenticate(username=username, password=password)
                login(request, user)
                data = {'data': serializer.data, 'logged in': True}
                print('Ba')
                return JsonResponse(data=data, status=status.HTTP_201_CREATED)
                #return redirect('profiles:checklogin')
            except:
                print('Bal')
            return JsonResponse(data=serializer.data, status=status.HTTP_201_CREATED)
        print('Ball')
        return JsonResponse(data=serializer.data, status=status.HTTP_400_BAD_REQUEST)
    else:
        print('Balls')
        return JsonResponse(data="Error", status=status.HTTP_400_BAD_REQUEST)
'''
# try catching csrf exceptions here and return a checked login function
@renderer_classes((JSONRenderer,))
@api_view(['POST'])
def login_account(request):
    """
        Use this view to log into an account without sending the username and password over
        basic auth.  This view also allows a user to login with either their username or email,
        but only one request needs to be sent.
    """
    context = {}
    logged_on = False
    if request.user.is_authenticated():
        print('hello its me')
        try:
            return redirect('profiles:checklogin')
        except:
            logged_on = True
            error = 'You are already logged in.'
            context['error'] = error
            context['logged_on'] = logged_on
            return JsonResponse(data=context, status=status.HTTP_200_OK)
    else:
        try:
            username = request.data['username_or_email']
            password = request.data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            logged_on = True
            context['logged_on'] = logged_on
            context['user'] = username
            return JsonResponse(data=context, status=status.HTTP_202_ACCEPTED)
        except:
            try:
                email = request.data['username_or_email']
                password = request.data['password']
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
                login(request, user)
                context['logged_on'] = True
                context['user'] = user_obj.username
                return JsonResponse(data=context, status=status.HTTP_202_ACCEPTED)
            except:
                context['error'] = "An error occured while validating your credentials. Please try again or create an account."
                context['logged_on'] = False
                return JsonResponse(data=context, status=status.HTTP_400_BAD_REQUEST)

@renderer_classes((JSONRenderer,))
@api_view(['GET'])
def logout_account(request):
    """
        This is an api view for logging a user out.  To log a user out, just send a get
        request to the profiles/logout/ url
    """
    context = {}
    logged_on = False
    if request.user.is_authenticated():
        logged_on = True
        try:
            logout(request)
            logged_on = False
            context['logged_on'] = logged_on
            return JsonResponse(data=context, status=status.HTTP_202_ACCEPTED)
        except:
            context['error'] = 'An error occured with logout'
            context['logged_on'] = logged_on
            return JsonResponse(data=context, status=status.HTTP_400_BAD_REQUEST)
    else:
        context['logged_on'] = logged_on
        return JsonResponse(data=context, status=status.HTTP_200_OK)


@api_view(['GET'])
def check_if_logged_in(request):
    """
        This view is made to check and see weather or not a user is logged in.
        This is mainly for testing purposes, but is also used by the user_creation_view,
        so do not edit or remove this view unless you redesign both views.
    """
    if request.user.username:
        try:
            data = {'username': request.user.username, 'logged in': True}
            return JsonResponse(data=data, status=status.HTTP_200_OK)
        except:
            print(request.user.username)
            data = {'logged in': False}
            return JsonResponse(data=data, status=status.HTTP_200_OK)
    else:
        data = {'logged in': False}
        return JsonResponse(data=data, status=status.HTTP_200_OK)
    return JsonResponse(data=data, status=status.HTTP_200_OK)


@renderer_classes((JSONRenderer,))
class MediaDetail(APIView):

    #authentication_classes = (SessionAuthentication, BasicAuthentication)
   # permission_classes = (IsAuthenticated,)

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
        musician = request.user.musician
        if request.user.musician.pk == self.user_pk:
            media = self.get_object(pk)
            media.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MediaListCreate(generics.ListCreateAPIView):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer


# To handle many to many fields that need to display, and be deleted by the user
#
# you will not be able to use django rest frameworks built in serializers and views.
#
# You will also need to build in a security feature for this.



"""
@csrf_exempt
@api_view(['POST'])
def media_create_api(request):
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


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def user_count_view(request, format=None):

    A view that returns the count of active users in JSON.

    user_count = User.objects.filter(active=True).count()
    content = {'user_count': user_count}
    return Response(content)
"""


@api_view(['GET'])
@renderer_classes((JSONRenderer,))
def render_comrades(request):
    """
        This is a view that sends a json array of data for use
        in the main feed.  Two fields in the data contain url of media files.
        This will be used in source tags for media rendering.
    """
    context = {}
    print('.......render_comrades .....musician....')
    logged_on = False
    if request.user.is_authenticated():
        visitor = request.user.musician
        logged_on = True
        comrades = visitor.comrades.all()
        musician_list = []
        media_list = []
        for com in reversed(comrades):
            muc = django_serializers.serialize("json", Musician.objects.filter(pk=com.numbre.numbre))
            musician = Musician.objects.get(pk=com.numbre.numbre)
            genres = [x.genre for x in musician.genres.all()]
            instruments = [x.name for x in musician.instruments.all()]
            if musician.media.all():
           # media = musician.latest_media().audio
                med = musician.media.all()[0]
                media = {'title': med.title,
                         'url': STATIC_URL[:-1] + med.audio.url}
            else:
                media = 'NONE'
            try:
                profile_img = STATIC_URL[:-1] + musician.profile_image.url
            except:
                profile_img = 'NONE'
            musicians = {'username': musician.user.username,
                         'first_name': musician.first_name,
                         'genres': genres,
                         'instruments': instruments,
                         'media': media,
                         'profile_image': profile_img

                         }
            musician_list.append(musicians)
        context['comrades'] = musician_list
    else:
        pass
    context['logged_on'] = logged_on
    return JsonResponse(data=context, status=status.HTTP_200_OK)#Response(context)


@api_view(['GET'])
def genre_choices(request):
    """
        This is a view for rendering the genre choices to the user.
        This will be used by the front end applications to limit the
        genres a user may choose.
    """
    choices = GENRES
    diction = {}
    li = []
    for data in choices:
        li.append(data[0])
    diction['GENRE_CHOICES'] = li
    return JsonResponse(data=diction, status=status.HTTP_200_OK)#, safe=False)

@csrf_exempt
@renderer_classes((JSONRenderer,))
@api_view(['POST', 'DELETE'])
def genre_add_delete_api(request):
    """
        This is view for adding or removing a genre from a users
        Genres field.
        To add a Genre send a POST request with the keyword 'Genre' and
        use the genre choices as a list of choices.
        To remove a genre send a DELETE request in the same format.
    """
    context = {}
    logged_on = False
    if request.user.is_authenticated():
        visitor = request.user.musician
        logged_on = True
        if request.method == "POST":
            try:
                name = request.data['Genre']
                genre = Genre.objects.get(genre=name)
                visitor.genres.add(genre)
                context['Genre'] = genre.genre
                context['Added'] = True
            except:
                context['Genre'] = "Please Select A Genre"
                context['Added'] = False
                context['logged_on'] = logged_on
                return JsonResponse(data=context, status=status.HTTP_400_BAD_REQUEST)
        if request.method == "DELETE":
            try:
                name = request.data['Genre']
                genre = Genre.objects.get(genre=name)
                visitor.genres.remove(genre)
                context['Genre'] = genre.genre
                context['Removed'] = True
            except:
                name = request.data['Genre']
                context['Genre'] = name
                context['Removed'] = False
                context['logged_on'] = logged_on
                return JsonResponse(data=context, status=status.HTTP_400_BAD_REQUEST)
    else:
        pass
    context['logged_on'] = logged_on
    return JsonResponse(data=context, status=status.HTTP_200_OK)

# When you get around to adding the instrument views, use the same technique as the genres,
#  but add in a ranking system so that you can show a more convenient list of instruments.
# Do a similar system for adding and removing friends.
# ##



@api_view(['GET'])
def instrument_choices(request):
    """
        This is a view for rendering the instrument choices to the user.
        This will be used by the front end applications to limit the
        instruments a user may choose. This works slightly different
        than genre choices.  This renders an ordered list of database table names.
    """
    #choices = INSTRUMENT_CLASSES
    choices = [x.name for x in Instrument.objects.all()]
    diction = {}
    li = []
    for data in choices:
        li.append(data)
    diction['INSTRUMENT_CHOICES'] = li
    return JsonResponse(data=diction, status=status.HTTP_200_OK)


@renderer_classes((JSONRenderer,))
@api_view(['POST', 'DELETE'])
def instrument_add_delete_api(request):
    """
        This is view for adding or removing an instrument from a users
        instruments field.
        To add an instrument send a POST request with the keyword 'Instrument' and
        use the instrument choices as a list of choices.
        To remove an instrument send a DELETE request in the same format.
    """
    context = {}
    logged_on = False
    if request.user.is_authenticated():
        visitor = request.user.musician
        logged_on = True
        if request.method == "POST":
            try:
                name = request.data['Instrument']
                instrument = Instrument.objects.get(name=name)
                visitor.instruments.add(instrument)
                context['Instrument'] = instrument.name
                context['Added'] = True
                instrument.numerator += 100
                update_instrument_rank(instrument)
            except:
                context['Instrument'] = "Please Select An Instrument"
                context['Added'] = False
                context['logged_on'] = logged_on
                return JsonResponse(data=context, status=status.HTTP_400_BAD_REQUEST)
        if request.method == "DELETE":
            try:
                name = request.data['Instrument']
                instrument = Instrument.objects.get(name=name)
                visitor.instruments.remove(instrument)
                context['Instrument'] = instrument.name
                context['Removed'] = True
                instrument.denominator += 1
            except:
                name = request.data['Instrument']
                context['Instrument'] = name
                context['Removed'] = False
                context['logged_on'] = logged_on
                return JsonResponse(data=context, status=status.HTTP_400_BAD_REQUEST)
    else:
        pass
    context['logged_on'] = logged_on
    return JsonResponse(data=context, status=status.HTTP_200_OK)

################
"""
Add an api view for updating all aspects of a users profile.
"""
################
