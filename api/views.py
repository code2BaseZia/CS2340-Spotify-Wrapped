import os, random, string
from django.shortcuts import render, redirect
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post, get
from .util import update_or_create_user_tokens, is_spotify_authenticated, link_user_token, spotify_request
from collections import Counter

# Create your views here.
class AuthURL(APIView):
    def get(self, request, format=None):
        scopes = 'user-top-read user-read-recently-played user-library-read user-follow-read playlist-read-private playlist-read-collaborative'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': os.getenv('REDIRECT_URI'),
            'client_id': os.getenv('SPOTIFY_CLIENT_ID')
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
        'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET')
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')
    print(error)

    if request.session.exists(request.session.session_key):
        request.session.create()
    update_or_create_user_tokens(request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('wrapped:link_token')


class IsAuthenticated(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request, format=None):
        if request.user is not None and request.user.is_authenticated:
            is_authenticated = is_spotify_authenticated(session_id=self.request.session.session_key, user=request.user)
        else:
            is_authenticated = is_spotify_authenticated(session_id=self.request.session.session_key)

        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


class LinkSpotifyToken(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request, format=None):
        if link_user_token(request.session.session_key, request.user):
            return Response({'message': 'Token successfully linked to user account'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Token does not exist'}, status=status.HTTP_400_BAD_REQUEST)


class UserStats(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request, format=None):
        term = request.GET.get('term')

        if term is None:
            return Response({'message': 'Please provide term for stats'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_spotify_authenticated(session_id=request.session.session_key, user=request.user):
            return Response({'message': 'User is not logged into Spotify.'}, status=status.HTTP_401_UNAUTHORIZED)

        tracks = spotify_request(request.user, 'me/top/tracks', params={
            'time_range': term,
            'limit': '50',
        })

        artists = spotify_request(request.user, 'me/top/artists', params={
            'time_range': term,
            'limit': '50',
        })
#Added a dictionary here to count albums
        albumCnt = Counter()
        albumTitles = [track['album']['name'] for track in tracks['items'] if track['album']['album_type'] == 'album' or
       (track['album']['album_type'] == 'single' and track['album']['total_tracks'] > 1)]
        rankFactor = 1
        for albumTitle in albumTitles:
            albumCnt[albumTitle] += rankFactor
            rankFactor -= .02

        topAlbums = albumCnt.most_common(5)
#Created a list for top artists and top tracks
        genreCnt = Counter()
        rankFactor = 1
        #counting genres (top genres) for each artist and for each genre count the genres and add them to our counter to decrement
        for artist in artists['items']:
            for genre in artist['genres']:
                genreCnt[genre] += rankFactor
            rankFactor -= 0.02

        topGenres = genreCnt.most_common(5)

        topArtists = [{'name': artist['name'], 'popularity': artist['popularity']} for artist in artists['items']]
        topTracks = [{'name': track['name'], 'popularity': track['popularity'], 'album': track['album']['name']} for track in tracks['items']]

        for item in tracks['items']:
            item['album'].pop('available_markets')
            item.pop('available_markets')

        response = {'tracks': tracks['items'], 'artists': artists['items'],  'topAlbums': topAlbums, 'topArtists': topArtists, 'topTracks':topTracks, 'topGenres':topGenres,}

        return Response(response, status=status.HTTP_200_OK)