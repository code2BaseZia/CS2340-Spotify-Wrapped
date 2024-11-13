from django.contrib import admin
from .models import Profile, Feedback, SpotifyUserWrap, TopTrackItem, TopAlbumItem, TopArtistItem, TopGenreItem
from api.models import SpotifyTrack, SpotifyArtist

# Register your models here.
admin.site.register(Profile)
admin.site.register(Feedback)


class TopTrackInLine(admin.TabularInline):
    model = TopTrackItem
    extra = 3


class TopArtistInLine(admin.TabularInline):
    model = TopArtistItem
    extra = 3


class WrappedAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'theme']})
    ]
    inlines = [TopTrackInLine, TopArtistInLine]
    list_display = ['user', 'theme']
    list_filter = ['created_at']


admin.site.register(TopTrackItem)
admin.site.register(TopAlbumItem)
admin.site.register(TopArtistItem)
admin.site.register(TopGenreItem)
admin.site.register(SpotifyUserWrap, WrappedAdmin)
