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


class TopAlbumInLine(admin.TabularInline):
    model = TopAlbumItem
    extra = 3


class TopGenreInLine(admin.TabularInline):
    model = TopGenreItem
    extra = 3


class WrappedAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['user', 'theme']}),
        ('More stats', {'fields': ['tracks_by_top_artist', 'top_track_by_top_artist', 'tracks_in_top_album',
                                   'top_track_in_top_album', 'top_track_by_top_artist_of_top_genre',
                                   'most_popular_track', 'track_popularity', 'average_popularity', 'ideal_key',
                                   'ideal_mode', 'average_duration', 'average_tempo', 'average_loudness',
                                   'average_danceability', 'average_energy', 'average_instrumentalness',
                                   'average_speechiness', 'average_valence', 'ideal_track']})
    ]
    inlines = [TopTrackInLine, TopArtistInLine, TopAlbumInLine, TopGenreInLine]
    list_display = ['user', 'theme']
    list_filter = ['created_at']


admin.site.register(TopTrackItem)
admin.site.register(TopAlbumItem)
admin.site.register(TopArtistItem)
admin.site.register(TopGenreItem)
admin.site.register(SpotifyUserWrap, WrappedAdmin)
