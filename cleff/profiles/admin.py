from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Musician, Genre, Media, ProfileModel, Location, Instrument, \
    SavedMusician, Comrade
# Register your models here.
admin.site.register(Genre)
admin.site.register(Media)
admin.site.register(Location)
admin.site.register(Instrument)
admin.site.register(Musician)
admin.site.register(SavedMusician)
admin.site.register(Comrade)



class MusicianInline(admin.StackedInline):
    model = Musician
    can_delete = False
    verbose_name_plural = 'musicians'
   # fk_name = 'user'



class ProfileAdmin(UserAdmin):
    inlines = (MusicianInline,)
    list_display = ('username',)
    list_filter = ('is_staff', 'is_superuser', 'is_active')



admin.site.unregister(User)  # Unregister user to add new inline ProfileInline
admin.site.register(User, ProfileAdmin)  # Register User with this inline profile
