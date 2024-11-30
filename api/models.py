from django.db import models


class SpotifyToken(models.Model):
    session = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)


class SpotifyArtist(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    followers = models.IntegerField(default=0)
    photo = models.URLField(max_length=500)
    popularity = models.IntegerField()
    url = models.URLField(max_length=500)


class SpotifyAlbum(models.Model):
    types = (
        ('album', 'Album'),
        ('single', 'Single'),
        ('compilation', 'Compilation'),
    )

    id = models.CharField(max_length=50, unique=True, primary_key=True)
    title = models.CharField(max_length=100)
    artists = models.ManyToManyField(SpotifyArtist, related_name='releases')
    photo = models.URLField(max_length=500)
    popularity = models.IntegerField()
    url = models.URLField(max_length=500)
    type = models.CharField(max_length=50, choices=types)
    date = models.CharField(max_length=10)
    total_tracks = models.PositiveIntegerField()


class SpotifyTrack(models.Model):
    id = models.CharField(max_length=50, unique=True, primary_key=True)
    title = models.CharField(max_length=100)
    artists = models.ManyToManyField(SpotifyArtist, related_name='tracks')
    album = models.ForeignKey(SpotifyAlbum, on_delete=models.CASCADE, related_name='tracks')
    preview = models.URLField(max_length=500, null=True, blank=True)
    popularity = models.PositiveIntegerField()
    url = models.URLField(max_length=500)
