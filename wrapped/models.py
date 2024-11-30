from django.db.models.signals import post_save
from django.contrib.auth.models import User
from api.models import SpotifyToken, SpotifyArtist, SpotifyTrack, SpotifyAlbum
from django.db import models
import random


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    token = models.OneToOneField(SpotifyToken, null=True, blank=True, on_delete=models.CASCADE)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


class Feedback(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    subject = models.CharField(max_length=100)
    message = models.CharField(max_length=10000)


post_save.connect(create_user_profile, sender=User)


class SpotifyUserWrap(models.Model):
    THEME = (
        ("no", "None"),
        ("ch", "Christmas"),
        ("hw", "Halloween"),
        ("ea", "Easter"),
    )
    TERMS = (
        ('short', '4 Weeks'),
        ('medium', '6 Months'),
        ('long', '1 Year'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(default="no", max_length=2, choices=THEME)
    # When the user who generated these wraps deletes their account, the on_delete will delete their wraps
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='wraps')
    term = models.CharField(max_length=6, choices=TERMS)
    public = models.BooleanField(default=False)

    tracks_by_top_artist = models.PositiveIntegerField(default=0)
    top_track_by_top_artist = models.ForeignKey(SpotifyTrack, on_delete=models.CASCADE,
                                                related_name='top_track_by_top_artist_wraps', blank=True, null=True)

    tracks_in_top_album = models.PositiveIntegerField(default=0)
    top_track_in_top_album = models.ForeignKey(SpotifyTrack, on_delete=models.CASCADE,
                                               related_name='top_track_in_top_album_wraps', blank=True, null=True)

    top_track_by_top_artist_of_top_genre = models.ForeignKey(SpotifyTrack, on_delete=models.CASCADE,
                                                             related_name='top_track_by_top_artist_of_top_genre_wraps',
                                                             blank=True, null=True)

    most_popular_track = models.ForeignKey(SpotifyTrack, on_delete=models.CASCADE,
                                           related_name='most_popular_track_wraps',
                                           blank=True, null=True)
    track_popularity = models.CharField(max_length=10, default='0000000000')
    average_popularity = models.FloatField(default=0)
    game_complete = models.BooleanField(default=False)


class TopTrackItem(models.Model):
    wrapped = models.ForeignKey(SpotifyUserWrap, on_delete=models.CASCADE, related_name='top_tracks')
    track = models.ForeignKey(SpotifyTrack, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']


class TopArtistItem(models.Model):
    wrapped = models.ForeignKey(SpotifyUserWrap, on_delete=models.CASCADE, related_name='top_artists')
    artist = models.ForeignKey(SpotifyArtist, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']


class TopAlbumItem(models.Model):
    wrapped = models.ForeignKey(SpotifyUserWrap, on_delete=models.CASCADE, related_name='top_albums')
    album = models.ForeignKey(SpotifyAlbum, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']


class TopGenreItem(models.Model):
    wrapped = models.ForeignKey(SpotifyUserWrap, on_delete=models.CASCADE, related_name='top_genres')
    name = models.CharField(max_length=100)
    freq = models.FloatField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']


class TopArtistOfGenre(models.Model):
    genre = models.ForeignKey(TopGenreItem, on_delete=models.CASCADE, related_name='top_artists')
    artist = models.ForeignKey(SpotifyArtist, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']


class TopTrackOfAlbum(models.Model):
    album = models.ForeignKey(TopAlbumItem, on_delete=models.CASCADE, related_name='top_tracks')
    track = models.ForeignKey(SpotifyTrack, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']


class HighLowGameQuestion(models.Model):
    wrapped = models.ForeignKey(SpotifyUserWrap, on_delete=models.CASCADE, related_name='highlow_game_questions')
    track = models.ForeignKey(SpotifyTrack, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()
    order = models.PositiveIntegerField()
    answer = models.IntegerField()

    class Meta:
        ordering = ['order']


class GuessingGameQuestion(models.Model):
    wrapped = models.ForeignKey(SpotifyUserWrap, on_delete=models.CASCADE, related_name='guess_game_questions')
    track = models.ForeignKey(SpotifyTrack, on_delete=models.CASCADE)
    rank = models.PositiveIntegerField()
    order = models.PositiveIntegerField()

    class Meta:
        ordering = ['order']


class WrappedSlide(models.Model):
    THEMES = (
        ('wrapped1', 'Default 1'),
        ('wrapped2', 'Default 2'),
        ('wrapped3', 'Default 3'),
        ('wrapped4', 'Default 4'),
        ('wrapped5', 'Default 5'),
        ('wrapped6', 'Default 6'),
        ('wrapped7', 'Default 7'),
    )
    LAYOUTS = (
        ('v1', 'Default 1'),
    )

    wrapped = models.ForeignKey(SpotifyUserWrap, on_delete=models.CASCADE, related_name='slides')
    number = models.PositiveIntegerField()
    colors = models.CharField(max_length=10, choices=THEMES, default=None, blank=True, null=True)
    layout = models.CharField(max_length=2, choices=LAYOUTS)

    def save(self, *args, **kwargs):
        if not self.colors:
            self.colors = random.choices(self.THEMES)[0][0]
        if not self.layout:
            self.layout = random.choices(self.LAYOUTS)[0][0]
        super(WrappedSlide, self).save(*args, **kwargs)

    class Meta:
        ordering = ['number']
