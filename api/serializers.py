from rest_framework import serializers
from wrapped.models import (SpotifyUserWrap, TopTrackItem, TopArtistItem, TopAlbumItem, TopGenreItem, TopArtistOfGenre,
                            TopTrackOfAlbum, WrappedSlide)
from .models import SpotifyTrack, SpotifyArtist, SpotifyAlbum


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyTrack
        fields = '__all__'
        depth = 2


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyArtist
        fields = '__all__'
        depth = 2


class ReleaseDateSerializer(serializers.IntegerField):
    def to_representation(self, value):
        print(value)
        return int(value.split('-')[0])


class AlbumSerializer(serializers.ModelSerializer):
    date = ReleaseDateSerializer()
    artists = ArtistSerializer(many=True, read_only=True)

    class Meta:
        model = SpotifyAlbum
        fields = '__all__'


class TrackOfAlbumSerializer(serializers.ListSerializer):
    child = TrackSerializer(read_only=True)

    def to_representation(self, instance):
        return [self.child.to_representation(item.track) for item in instance.all()]


class ArtistOfGenreSerializer(serializers.ListSerializer):
    child = ArtistSerializer(read_only=True)

    def to_representation(self, instance):
        return [self.child.to_representation(item.artist) for item in instance.all()]

    class Meta:
        depth = 2


class AlbumItemSerializer(serializers.ModelSerializer):
    top_tracks = TrackOfAlbumSerializer(read_only=True)
    album = AlbumSerializer(read_only=True)

    class Meta:
        model = TopAlbumItem
        fields = ['album', 'top_tracks']
        depth = 2


class GenreItemSerializer(serializers.ModelSerializer):
    top_artists = ArtistOfGenreSerializer(read_only=True)

    class Meta:
        model = TopGenreItem
        fields = ['name', 'top_artists']
        depth = 2


class TrackItemSerializer(serializers.ListSerializer):
    child = TrackSerializer(read_only=True)

    def to_representation(self, instance):
        return [self.child.to_representation(item.track) for item in instance.all()]


class ArtistItemSerializer(serializers.ListSerializer):
    child = ArtistSerializer(read_only=True)

    def to_representation(self, instance):
        return [self.child.to_representation(item.artist) for item in instance.all()]


class SlidesSerializer(serializers.ModelSerializer):
    number = serializers.CharField()

    class Meta:
        model = WrappedSlide
        exclude = ('wrapped',)


class PopularitySerializer(serializers.ListSerializer):
    child = serializers.IntegerField()

    def to_representation(self, instance):
        return [int(instance[2 * i:2 * i + 2]) for i in range(5)]


class MaxPopularitySerializer(serializers.IntegerField):
    def to_representation(self, instance):
        return max([int(instance[2 * i:2 * i + 2]) for i in range(5)])


class KeySerializer(serializers.CharField):
    def to_representation(self, instance):
        KEYS = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B', 'None']
        return KEYS[instance]


class ModeSerializer(serializers.CharField):
    def to_representation(self, instance):
        return 'M' if instance == 1 else 'm'


class WrappedSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.user.username', read_only=True)
    url = serializers.HyperlinkedIdentityField(view_name='wrapped:wrap', lookup_field='pk')
    top_tracks = TrackItemSerializer(read_only=True)
    top_artists = ArtistItemSerializer(read_only=True)
    top_albums = AlbumItemSerializer(many=True, read_only=True)
    top_genres = GenreItemSerializer(many=True, read_only=True)
    slides = SlidesSerializer(many=True, read_only=True)
    track_popularity = PopularitySerializer(read_only=True)
    max_popularity = MaxPopularitySerializer(source='track_popularity', read_only=True)
    ideal_key = KeySerializer(read_only=True)
    ideal_mode = ModeSerializer(read_only=True)

    class Meta:
        model = SpotifyUserWrap
        fields = '__all__'
        depth = 3
