from django.contrib.auth.models import User
from profiles.models import Musician, Location, SavedMusician, Comrade
from django.contrib.gis.geos import Point
from django.http import HttpResponse, JsonResponse
from haystack.query import SearchQuerySet
from haystack.utils.geo import Distance

from django.shortcuts import render, redirect

# Create your views here.

# This view takes a Post request with coordinates and finds users in their area
def update_comrades_view(request):
    if request.POST:
        cor_data = request.POST['coordinates']
        if request.user.musician:
            user = request.user.musician
            user.current_location = cor_data
            user.save()
            coor = user.current_location
            print(coor)
            lat = float(coor.latitude)
            lon = float(coor.longitude)
            current_location = Point(lon, lat)
            radius = user.search_range
            max_dist = Distance(mi=radius)
            loc_match = SearchQuerySet().dwithin(
                'location',
                current_location,
                max_dist)
            com_list = []
            if len(loc_match) > 0:
                for obj in loc_match:
                    print("obj: {}".format(obj.pk))
                    try:
                        loc_o_user = Musician.objects.get(pk=obj.pk)
                        if loc_o_user != user:
                            try:
                                sav = SavedMusician.objects.filter(numbre=loc_o_user.pk,
                                                                   saver_musician=request.user.musician)[0]
                                try:
                                    com = Comrade.objects.filter(numbre=sav)[0]
                                    com_list.append(com)
                                except:
                                    com = Comrade.objects.create(numbre=sav)
                                    com_list.append(com)
                            except:
                                sav = SavedMusician.objects.create(numbre=loc_o_user.pk,
                                                                   saver_musician=request.user.musician)
                                sav.save()
                                com = Comrade.objects.create(numbre=sav)
                                com.save()
                                com_list.append(com)
                            try:
                                if com in user.comrades.all():
                                    print('Com {} already in {}s comrade list'.format(
                                        com,
                                        user))
                                    pass
                                else:
                                    user.comrades.add(com)
                                    user.save()
                            except:
                                user.comrades.add(com)
                                user.save()
                    except:
                        pass
                if com_list:
                    for co in user.comrades.all():
                        if co not in com_list:
                            print('should remove {} from {}.comrades'.format(co, user))
                            user.comrades.remove(co)
                else:
                    pass
            return HttpResponse('success', status=200)
    else:
        return HttpResponse('Method Not Allowed', status=405)
