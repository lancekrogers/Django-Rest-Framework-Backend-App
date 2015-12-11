from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView

from profiles.models import Musician
from .models import TheConversation, Message

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
    model = TheConversation

    def owner_is_musician_one(self):
        owner = Musician.objects.get(pk=self.request.user.pk)
        return TheConversation.objects.filter(musician_one=owner)

    def owner_is_musician_two(self):
        owner = Musician.objects.get(pk=self.request.user.pk)
        return TheConversation.objects.filter(musician_two=owner)

    def get_queryset(self):
        profile = Musician.objects.get(user=self.request.user)
        return TheConversation.objects.filter(Q(musician_one=profile) | Q(musician_two=profile))


class MusicianMusicianConversationDetailView(DetailView):
    model = TheConversation
    fields = ['messages']

    def list_of_messages(self):
        return TheConversation.messages



# After the message is created add a "link" to the conversation
# This may be implemented only on the front end, but possibly on the
# back end after implementation is figured out.
@renderer_classes((JSONRenderer,))
@api_view(['POST'])
def message_create(request):
    """
    This view is for sending messages.  It looks for existing conversations and if they are
    not there it creates a conversation and a message.
    """
    context = {}
    logged_on = False
    if request.user.is_authenticated():
        logged_on = True
        if request.method == 'POST':
            message_t = request.data['message']
            reciever_name = request.data['reciever_username']
            r_user = User.objects.get(username=reciever_name)
            receiver = Musician.objects.get(user=r_user)  # This may or may not work
            me = request.user.musician
            mm_message = Message.objects.create(
                sender=me,
                receiver=receiver,
                message=message_t
            )
            mm_message.save()
            try:
                if not TheConversation.objects.get(Q(musician_one=me, musician_two=receiver) | Q(musician_one=receiver, musician_two=me)):
                    conv = TheConversation.objects.create(musician_one=me, musician_two=receiver)
                    conv.messages.add(mm_message)
                    conv.save()
                    return render(request, context)
                else:
                    conv = TheConversation.objects.get(Q(musician_one=me, musician_two=receiver) | Q(musician_one=receiver, musician_two=me))
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


@renderer_classes((JSONRenderer,))
@api_view(['DELETE'])
def conversation_delete(request):
    context = {}
    deleted = False
    logged_on = False
    context['logged_on'] = logged_on
    if request.user.is_authenticated():
        logged_on = True
        try:
            sender = request.data['Sender']
            receiver = request.data['Receiver']
            context['deleted'] = deleted
            if request.method == 'DELETE':
                instance = TheConversation.objects.get(Q(musician_one=sender,
                                                                      musician_two=receiver) | Q(musician_one=receiver, musician_two=sender))
                context['conversation'] = instance
                instance.delete()
                deleted = True
                context['deleted'] = deleted
                return JsonResponse(data=context, status=status.HTTP_202_ACCEPTED)
        except:
            context['error'] = 'Please submit a sender and receiver'
            return JsonResponse(data=context, status=status.HTTP_400_BAD_REQUEST)
    else:
        return JsonResponse(data=context, status=status.HTTP_400_BAD_REQUEST)