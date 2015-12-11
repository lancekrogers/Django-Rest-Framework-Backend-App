from django.db import models
from django.conf import settings
from profiles.models import Musician

# Create your models here.


class TheConversation(models.Model):
    initializer = models.ForeignKey(Musician, related_name='initializer')
    musician_one = models.ForeignKey(Musician, related_name='musician_one')
    musician_two = models.ForeignKey(Musician, related_name='musician_two')
    messages = models.ManyToManyField('Message', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return 'conversation between {} and {}'.format(self.musician_one, self.musician_two)


class Message(models.Model):
    message = models.TextField()
    conversation = models.ManyToManyField(TheConversation)
    sender = models.ForeignKey(Musician, related_name='sender')
    receiver = models.ForeignKey(Musician, related_name='receiver')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} {}'.format(self.conversation, self.timestamp)

    class Meta:
        ordering = ['-timestamp']