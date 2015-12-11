from .models import Message, TheConversation
from django.contrib import admin

# Register your models here.
admin.site.register(TheConversation)
admin.site.register(Message)