from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, DeleteView

from cleff.profiles.models import Musician
from .models import MusicianMusicianConversation, MusMusMessage

# Create your views here.


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


def mm_message_create_view(request, conversation_pk, receiver_pk):
    message_t = request.POST['memo']
    conv = MusicianMusicianConversation.objects.get(pk=conversation_pk)
    receiver = Musician.objects.get(pk=receiver_pk)
    me = request.user.musician
    if request.method == 'POST':
        print('mm_message_create POST')
        mm_message = MusMusMessage.objects.create(
            sender=me,
            receiver=receiver,
            message=message_t
        )
        mm_message.save()
        print('mm_message saved')
        conv.messages.add(mm_message)
        conv.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'messaging/musicianmusicianconversation_detail.html',
                  {'message_form': message_t})


def conversation_delete(request, conversation_pk):
    if request.POST:
        instance = MusicianMusicianConversation.objects.get(pk=conversation_pk)
        instance.delete()
        return redirect('message:musician_conversations')
