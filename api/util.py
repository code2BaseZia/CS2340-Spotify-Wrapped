from .models import SpotifyToken, SpotifyTrack, SpotifyArtist, SpotifyAlbum
from wrapped.models import SpotifyUserWrap, TopTrackItem, TopArtistItem
from django.utils import timezone
from datetime import timedelta
from requests import post, put, get
import os

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


def get_or_create_artist(user, id):
    artists = SpotifyArtist.objects.filter(id=id)
    if artists.exists():
        return artists.first()
    else:
        response = spotify_request(user, 'artists/' + id)
        artist = SpotifyArtist(id=id, name=response['name'], followers=response['followers']['total'],
                               photo=response['images'][0]['url'], popularity=response['popularity'])
        artist.save()
        return artist


def get_or_create_album(user, id):
    albums = SpotifyTrack.objects.filter(id=id)
    if albums.exists():
        return albums.first()
    else:
        response = spotify_request(user, 'albums/' + id)
        album = SpotifyAlbum(id=id, title=response['name'], photo=response['images'][0]['url'], popularity=response['popularity'])
        album.save()
        for item in response['artists']:
            album.artists.add(get_or_create_artist(user, item['id']))
        return album


def get_or_create_track(user, id):
    tracks = SpotifyTrack.objects.filter(id=id)
    if tracks.exists():
        return tracks.first()
    else:
        response = spotify_request(user, 'tracks/' + id)
        features = spotify_request(user, 'audio-features/' + id)

        track = SpotifyTrack(id=id, title=response['name'], popularity=response['popularity'],
                             album=get_or_create_album(user, response['album']['id']), preview=response['preview_url'],
                             duration=features['duration_ms'], key=features['key'], mode=features['mode'],
                             tempo=features['tempo'], loudness=features['loudness'],danceability=features['danceability'],
                             energy=features['energy'], instrumentalness=features['instrumentalness'],
                             speechiness=features['speechiness'], valence=features['valence'])
        track.save()
        print(response['artists'])
        for item in response['artists']:
            print(item['id'])
            track.artists.add(get_or_create_artist(user, item['id']))
        return track


def create_wrapped(user, term):
    wrapped = SpotifyUserWrap(user=user.profile)
    wrapped.save()

    tracks = spotify_request(user, 'me/top/tracks', params={
        'time_range': term,
        'limit': '50',
    })

    artists = spotify_request(user, 'me/top/artists', params={
        'time_range': term,
        'limit': '50',
    })

    for i in range(5):
        track = get_or_create_track(user, tracks['items'][i]['id'])
        top_track = TopTrackItem(wrapped=wrapped, track=track, order=i)

        artist = get_or_create_artist(user, artists['items'][i]['id'])
        top_artist = TopArtistItem(wrapped=wrapped, artist=artist, order=i)

        top_track.save()
        top_artist.save()

    return wrapped.id
