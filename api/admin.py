from django.contrib import admin
from .models import SpotifyToken, SpotifyTrack, SpotifyAlbum, SpotifyArtist

# Register your models here.
admin.site.register(SpotifyToken)
admin.site.register(SpotifyTrack)
admin.site.register(SpotifyAlbum)
admin.site.register(SpotifyArtist)
