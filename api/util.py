from django.db import transaction

from .models import SpotifyToken, SpotifyTrack, SpotifyArtist, SpotifyAlbum
from wrapped.models import (SpotifyUserWrap, TopTrackItem, TopArtistItem, TopAlbumItem, TopGenreItem, TopArtistOfGenre,
                            TopTrackOfAlbum, WrappedSlide)
from django.utils import timezone
from datetime import timedelta
from requests import post, put, get
import os
from collections import Counter
from django.db.models import Q
from django.templatetags.static import static

BASE_URL = 'https://api.spotify.com/v1/'


def get_user_tokens(session_id=None, user=None):
    if user is not None:
        return user.profile.token
    if session_id is not None:
        user_tokens = SpotifyToken.objects.filter(session=session_id)
        if not user_tokens.exists():
            return None
        return user_tokens[0]
    return None


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token, user=None):
    tokens = get_user_tokens(session_id, user)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token', 'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(session=session_id, access_token=access_token, refresh_token=refresh_token,
                              token_type=token_type, expires_in=expires_in)
        tokens.save()

        if user is not None:
            profile = user.profile
            profile.token = tokens
            profile.save(update_fields=['token'])


def is_spotify_authenticated(session_id=None, user=None):
    tokens = get_user_tokens(session_id, user)
    if not tokens:
        return False

    expiry = tokens.expires_in

    if expiry <= timezone.now():
        refresh_spotify_token(tokens, user)

    return True


def refresh_spotify_token(tokens, user=None):
    refresh_token = tokens.refresh_token
    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
        'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    # If this doesn't work, he changes the method to use session_id instead of passing in tokens
    update_or_create_user_tokens(tokens.session, access_token, token_type, expires_in, refresh_token, user)


def link_user_token(session_id, user):
    tokens = get_user_tokens(session_id)
    if not tokens:
        return False

    expiry = tokens.expires_in

    if expiry <= timezone.now():
        refresh_spotify_token(tokens, user)

    profile = user.profile
    profile.token = tokens
    profile.save(update_fields=['token'])

    return True


def spotify_request(user, endpoint, post_=False, put_=False, params=None, body=None):
    tokens = get_user_tokens(user=user)
    headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + tokens.access_token}

    if post_:
        post(BASE_URL + endpoint, headers=headers, data=body, params=params)
    if put_:
        put(BASE_URL + endpoint, headers=headers, data=body, params=params)

    response = get(BASE_URL + endpoint, headers=headers, params=params)
    try:
        return response.json()
    except:
        return {'Error': 'Issue with request'}


def get_or_create_artist(user, id, data=None):
    artists = SpotifyArtist.objects.filter(id=id)
    if artists.exists():
        return artists.first()
    else:
        response = spotify_request(user, 'artists/' + id) if data is None else data
        image = static('wrapped/img/placeholder.png') if len(response['images']) == 0 else response['images'][0]['url']
        artist = SpotifyArtist(id=id, name=response['name'], followers=response['followers']['total'],
                               photo=image, popularity=response['popularity'], url=response['external_urls']['spotify'])
        artist.save()
        return artist


def get_or_create_album(user, id, data=None):
    albums = SpotifyTrack.objects.filter(id=id)
    if albums.exists():
        return albums.first()
    else:
        response = spotify_request(user, 'albums/' + id) if data is None else data
        image = static('wrapped/img/placeholder.png') if len(response['images']) == 0 else response['images'][0]['url']
        album = SpotifyAlbum(id=id, title=response['name'], photo=image, popularity=response['popularity'],
                             url=response['external_urls']['spotify'], type=response['album_type'],
                             date=response['release_date'], total_tracks=response['tracks']['total'])
        album.save()
        for item in response['artists']:
            album.artists.add(get_or_create_artist(user, item['id']))
        return album


def get_or_create_track(user, id, data=None):
    tracks = SpotifyTrack.objects.filter(id=id)
    if tracks.exists():
        return tracks.first()
    else:
        response, features = (spotify_request(user, 'tracks/' + id), spotify_request(user, 'audio-features/' + id)) if data is None else data

        track = SpotifyTrack(id=id, title=response['name'], popularity=response['popularity'],
                             album=get_or_create_album(user, response['album']['id']), preview=response['preview_url'],
                             url=response['external_urls']['spotify'], duration=features['duration_ms'],
                             key=features['key'], mode=features['mode'], tempo=features['tempo'],
                             loudness=features['loudness'],danceability=features['danceability'],
                             energy=features['energy'], instrumentalness=features['instrumentalness'],
                             speechiness=features['speechiness'], valence=features['valence'])
        track.save()
        print(response['artists'])
        for item in response['artists']:
            print(item['id'])
            track.artists.add(get_or_create_artist(user, item['id']))
        return track


def create_items(user, tracks=None, artists=None, albums=None):
    if artists is not None:
        artists_data = spotify_request(user, 'artists', params={'ids': ','.join(artists)})
        for artist in artists_data['artists']:
            get_or_create_artist(user, artist['id'], artist)
    if albums is not None:
        albums_data = spotify_request(user, 'albums', params={'ids': ','.join(albums)})
        for album in albums_data['albums']:
            get_or_create_album(user, album['id'], album)
    if tracks is not None:
        tracks_data = spotify_request(user, 'tracks', params={'ids': ','.join(tracks)})
        features = spotify_request(user, 'audio-features', params={'ids': ','.join(tracks)})
        for i in range(len(tracks)):
            get_or_create_track(user, tracks[i], (tracks_data['tracks'][i], features['audio_features'][i]))


def calculate_top_albums_and_genres(tracks, artists):
    album_count = Counter()
    album_ids = [track['album']['id'] for track in tracks if track['album']['total_tracks'] > 1]
    rank_factor = 1
    for album_id in album_ids:
        album_count[album_id] += rank_factor
        rank_factor -= .02

    top_albums = album_count.most_common(10)

    genre_count = Counter()
    rank_factor = 1
    for artist in artists:
        for genre in artist['genres']:
            genre_count[genre] += rank_factor
        rank_factor -= .02

    top_genres = genre_count.most_common(10)

    return top_albums, top_genres


def add_top_tracks_and_artists(user, wrapped, tracks, artists):
    top_tracks, top_artists = [], []
    for i in range(5):
        track = get_or_create_track(user, tracks[i]['id'])
        top_track = TopTrackItem(wrapped=wrapped, track=track, order=i)
        top_tracks.append(track.id)

        artist = get_or_create_artist(user, artists[i]['id'])
        top_artist = TopArtistItem(wrapped=wrapped, artist=artist, order=i)
        top_artists.append(artist.id)

        top_track.save()
        top_artist.save()

    return top_tracks, top_artists


def add_top_albums_and_genres(user, wrapped, albums, genres):
    for i in range(4):
        album_item = TopAlbumItem(wrapped=wrapped, album=get_or_create_album(user, albums[i][0]), order=i)
        album_item.save()

    for i in range(10):
        frequency = genres[i][1] / genres[0][1]
        genre_item = TopGenreItem(wrapped=wrapped, name=genres[i][0], freq=frequency, order=i)
        genre_item.save()

    return [albums[i][0] for i in range(4)], [x[0] for x in genres]


def get_top_artists_per_genre(user, wrapped, artists, genres):
    top_artists_of_genre = [[], [], [], [], [], [], [], [], [], []]
    for artist in artists:
        intersection = set(artist['genres']) & set(genres)
        if len(intersection) > 0:
            api_artist = get_or_create_artist(user, artist['id'])
            for item in intersection:
                index = genres.index(item)
                new_index = len(top_artists_of_genre[index])
                if new_index < 3:
                    genre_item = TopGenreItem.objects.filter(wrapped=wrapped, order=index).first()
                    genre_artist = TopArtistOfGenre(genre=genre_item, artist=api_artist, order=new_index)
                    genre_artist.save()
                    top_artists_of_genre[index].append(api_artist)

    return top_artists_of_genre


def get_popularity_rank(popularity):
    if popularity > 80:
        return 4
    if popularity > 60:
        return 3
    if popularity > 40:
        return 2
    if popularity > 20:
        return 1
    return 0


def find_ideal_track(key, features):
    min_cost = -1
    ideal_track = None

    with transaction.atomic():
        for track in SpotifyTrack.objects.all().iterator():
            if track.key != key[0] or track.mode != key[1]:
                continue

            cost = ((features['duration'] - track.duration) / 195000) ** 2 \
                 + ((features['tempo'] - track.tempo) / 120) ** 2 \
                 + ((features['loudness'] - track.loudness) / 14) ** 2 \
                 + (features['danceability'] - track.danceability) ** 2 \
                 + (features['energy'] - track.energy) ** 2 \
                 + (features['instrumentalness'] - track.instrumentalness) ** 2 \
                 + (features['speechiness'] - track.speechiness) ** 2 \
                 + (features['valence'] - track.valence) ** 2

            if min_cost < 0 or cost < min_cost:
                min_cost = cost
                ideal_track = track

    return ideal_track


def create_wrapped(user, term):
    wrapped = SpotifyUserWrap(user=user.profile, term=term)
    wrapped.save()

    all_tracks = spotify_request(user, 'me/top/tracks', params={
        'time_range': term + '_term',
        'limit': '50',
    })

    all_artists = spotify_request(user, 'me/top/artists', params={
        'time_range': term + '_term',
        'limit': '50',
    })

    all_albums, all_genres = calculate_top_albums_and_genres(all_tracks['items'], all_artists['items'])

    create_items(user=user, tracks=[track['id'] for track in all_tracks['items']], artists=[artist['id'] for artist in all_artists['items']], albums=[x[0] for x in all_albums])

    tracks, artists = add_top_tracks_and_artists(user, wrapped, all_tracks['items'], all_artists['items'])
    albums, genres = add_top_albums_and_genres(user, wrapped, all_albums, all_genres)
    genre_artists = get_top_artists_per_genre(user, wrapped, all_artists['items'], genres)

    tracks_by_top_artist = 0
    top_track_by_top_artist = None

    tracks_in_top_album = 0
    top_track_in_top_album = None

    top_track_by_top_artist_of_top_genre = None

    most_popular_track = None
    track_popularity = [0] * 5
    average_popularity = 0

    keys = Counter()
    average_features = {
        'duration': 0,
        'tempo': 0,
        'loudness': 0,
        'danceability': 0,
        'energy': 0,
        'instrumentalness': 0,
        'speechiness': 0,
        'valence': 0
    }

    rank_factor = 1

    for track in all_tracks['items']:
        api_track = get_or_create_track(user, track['id'])

        popularity = api_track.popularity
        track_popularity[get_popularity_rank(popularity)] += 1
        average_popularity += popularity
        if most_popular_track is None or popularity > most_popular_track.popularity:
            most_popular_track = api_track

        average_features['duration'] += api_track.duration * rank_factor
        average_features['tempo'] += api_track.tempo * rank_factor
        average_features['loudness'] += api_track.loudness * rank_factor
        average_features['danceability'] += api_track.danceability * rank_factor
        average_features['energy'] += api_track.energy * rank_factor
        average_features['instrumentalness'] += api_track.instrumentalness * rank_factor
        average_features['speechiness'] += api_track.speechiness * rank_factor
        average_features['valence'] += api_track.valence * rank_factor

        keys[(api_track.key, api_track.mode)] += rank_factor

        rank_factor -= .02

        if any([artist['id'] == artists[0] for artist in track['artists']]):
            tracks_by_top_artist += 1
            if top_track_by_top_artist is None:
                top_track_by_top_artist = api_track

        if any([artist['id'] == genre_artists[0][0].id for artist in track['artists']]):
            if top_track_by_top_artist_of_top_genre is None:
                top_track_by_top_artist_of_top_genre = api_track

        if track['album']['id'] in albums:
            album_id = track['album']['id']
            index = albums.index(album_id)

            if index == 0:
                tracks_in_top_album += 1
                if top_track_in_top_album is None:
                    top_track_in_top_album = api_track

            album_item = TopAlbumItem.objects.filter(wrapped=wrapped, order=index).first()
            new_index = album_item.top_tracks.count()
            if new_index < 3:
                album_track = TopTrackOfAlbum(album=album_item, track=api_track, order=new_index)
                album_track.save()

    average_popularity /= 50

    average_features['duration'] /= 25.5
    average_features['tempo'] /= 25.5
    average_features['loudness'] /= 25.5
    average_features['danceability'] /= 25.5
    average_features['energy'] /= 25.5
    average_features['instrumentalness'] /= 25.5
    average_features['speechiness'] /= 25.5
    average_features['valence'] /= 25.5

    wrapped.tracks_by_top_artist = tracks_by_top_artist
    wrapped.top_track_by_top_artist = top_track_by_top_artist
    wrapped.tracks_in_top_album = tracks_in_top_album
    wrapped.top_track_in_top_album = top_track_in_top_album
    wrapped.top_track_by_top_artist_of_top_genre = top_track_by_top_artist_of_top_genre
    wrapped.most_popular_track = most_popular_track
    wrapped.track_popularity = ''.join([f'{frq:02}' for frq in track_popularity])
    wrapped.average_popularity = average_popularity

    ideal_key = keys.most_common()[0][0]

    wrapped.ideal_key = ideal_key[0]
    wrapped.ideal_mode = ideal_key[1]
    wrapped.average_duration = average_features['duration']
    wrapped.average_tempo = average_features['tempo']
    wrapped.average_loudness = average_features['loudness']
    wrapped.average_danceability = average_features['danceability']
    wrapped.average_energy = average_features['energy']
    wrapped.average_instrumentalness = average_features['instrumentalness']
    wrapped.average_speechiness = average_features['speechiness']
    wrapped.average_valence = average_features['valence']

    wrapped.ideal_track = find_ideal_track(ideal_key, average_features)

    for i in range(11):
        slide = WrappedSlide(wrapped=wrapped, number=i)
        slide.save()

    wrapped.save()

    return wrapped.id


def get_all_user_wraps(user):
    wraps = SpotifyUserWrap.objects.filter(user=user.profile).all()
    return wraps


def get_wrap_by_id(user, wrap_id):
    if user is None:
        wrap = SpotifyUserWrap.objects.filter(id=wrap_id, public=True)
    else:
        wrap = SpotifyUserWrap.objects.filter(Q(id=wrap_id), Q(public=True) | Q(user=user.profile))

    if not wrap.exists():
        return 'Wrap does not exist, or is private and not owned by you'
    return wrap.first()
