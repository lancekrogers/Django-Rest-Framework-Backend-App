from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView

from profiles.models import Musician
from .models import MusicianMusicianConversation, MusMusMessage

# Create your views here.
from rest_framework import status
from rest_framework.decorators import renderer_classes, api_view
from rest_framework.renderers import JSONRenderer
"""
You need major renovation of this app.  What you need to do is take the conversation starter
function and the message creation functions and have them be in one api view.  Check to see if
a conversation exist and if it doesn't then create one, if there is already a converstation take
them to that conversation and create a new message in that conversation.
"""

class MusicianMusicianConversationListView(ListView):
    model = MusicianMusicianConversation

    def owner_is_musician_one(self):
        owner = Musician.objects.get(pk=self.request.user.pk)
        return MusicianMusicianConversation.objects.filter(musician_one=owner)

    def owner_is_musician_two(self):
        owner = Musician.objects.get(pk=self.request.user.pk)
        return MusicianMusicianConversation.objects.filter(musician_two=owner)

    def get_queryset(self):
        profile = Musician.objects.get(user=self.request.user)
        return MusicianMusicianConversation.objects.filter(Q(musician_one=profile) | Q(musician_two=profile))


class MusicianMusicianConversationDetailView(DetailView):
    model = MusicianMusicianConversation
    fields = ['messages']

    def list_of_messages(self):
        return MusicianMusicianConversation.messages


def mm_start_conv(request, receiver_pk):
    me = Musician.objects.get(pk=request.user.pk)
    print(me)
    other = Musician.objects.get(pk=receiver_pk)
    print(other)
    redirection = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        print('post mm_start_conv')
        if not MusicianMusicianConversation.objects.filter(Q(musician_one=me, musician_two=other) |
                                                           Q(musician_one=other, musician_two=me)):
            obj = MusicianMusicianConversation.objects.create(
                initializer=me,
                musician_one=me,
                musician_two=other,
            )
            obj.save()
            return redirect('message:musician_conv_detail_view', obj.pk)
        else:
            obj = MusicianMusicianConversation.objects.get(Q(musician_one=me, musician_two=other) |
                                                           Q(musician_one=other, musician_two=me))
            return redirect('message:musician_conv_detail_view', obj.pk)
    else:
        print('doesnt work')
        return HttpResponseRedirect(redirection)

@renderer_classes((JSONRenderer,))
@api_view(['POST'])
def message_create(request):
    context = {}
    logged_on = False
    if request.user.is_authenticated():
        sender = request.user.musician()
        logged_on = True
        if request.method == 'POST':
            message_t = request.POST['message']
            reciever_name = request.POST['reciever']
            r_user = User.objects.get(username=reciever_name)
            receiver = Musician.objects.get(user=r_user)  # This may or may not work
            me = request.user.musician
            mm_message = MusMusMessage.objects.create(
                sender=me,
                receiver=receiver,
                message=message_t
            )
            mm_message.save()
            try:
                if not MusicianMusicianConversation.objects.get(Q(musician_one=me, musician_two=receiver) | Q(musician_one=receiver, musician_two=me)):
                    conv = MusicianMusicianConversation.objects.create(musician_one=me, musician_two=receiver)
                    conv.messages.add(mm_message)
                    conv.save()
                    return render(request, context)
                else:
                    conv = MusicianMusicianConversation.objects.get(Q(musician_one=me, musician_two=receiver) | Q(musician_one=receiver, musician_two=me))
                    conv.messages.add(mm_message)
                    conv.save()
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            except:
                context['error'] = 'There is an error in lines 88-92 in your message views'
                context['logged_on'] = logged_on
                return JsonResponse(data=context, status=status.HTTP_403_FORBIDDEN)

        else:
            context['logged_on'] = logged_on
            return JsonResponse(data=context, status=status.HTTP_403_FORBIDDEN)
    context['logged_on'] = logged_on
    return JsonResponse(data=context, status=status.HTTP_200_OK)


def conversation_delete(request, conversation_pk):
    if request.POST:
        instance = MusicianMusicianConversation.objects.get(pk=conversation_pk)
        instance.delete()
        return redirect('message:musician_conversations')