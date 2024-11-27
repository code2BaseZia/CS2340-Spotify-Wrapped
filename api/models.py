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

    duration = models.PositiveIntegerField()
    key = models.IntegerField()
    mode = models.IntegerField()
    tempo = models.IntegerField()
    loudness = models.FloatField()

    # Danceability describes how suitable a track is for dancing based on a combination of musical elements including
    # tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most
    # danceable.
    danceability = models.FloatField()
    # Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically,
    # energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores
    # low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness,
    # timbre, onset rate, and general entropy.
    energy = models.FloatField()
    # Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context.
    # Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater
    # likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks,
    # but confidence is higher as the value approaches 1.0.
    instrumentalness = models.FloatField()
    # Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g.
    # talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are
    # probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music
    # and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely
    # represent music and other non-speech-like tracks.
    speechiness = models.FloatField()
    # A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound
    # more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad,
    # depressed, angry).
    valence = models.FloatField()
