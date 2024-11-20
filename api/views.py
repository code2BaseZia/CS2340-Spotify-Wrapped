import os, random, string
from django.shortcuts import render, redirect
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from requests import Request, post, get
from .util import (update_or_create_user_tokens, is_spotify_authenticated, link_user_token, spotify_request,
                   create_wrapped, get_all_user_wraps, get_wrap_by_id, calculate_top_albums_and_genres)
from .serializers import WrappedSerializer

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
            'time_range': term + '_term',
            'limit': '50',
        })

        artists = spotify_request(request.user, 'me/top/artists', params={
            'time_range': term + '_term',
            'limit': '50',
        })

        top_albums, top_genres = calculate_top_albums_and_genres(tracks['items'], artists['items'])

        albums = spotify_request(request.user, 'albums', params={
            'ids': ','.join([album[0] for album in top_albums])
        })

        for item in tracks['items']:
            item['album'].pop('available_markets')
            item.pop('available_markets')

        for item in albums['albums']:
            item.pop('available_markets')
            item.pop('tracks')

        response = {
            'tracks': tracks['items'], 'artists': artists['items'],
            'albums': albums['albums'],
            'genres': [{'name': genre[0], 'freq': genre[1] / top_genres[0][1]} for genre in top_genres]
        }

        return Response(response, status=status.HTTP_200_OK)


class UserWrapped(APIView):
    authentication_classes = [SessionAuthentication]

    def post(self, request, format=None):
        term = request.data.get('term')

        if term is None:
            return Response({'message': 'Please provide term for stats'}, status=status.HTTP_400_BAD_REQUEST)

        if not is_spotify_authenticated(session_id=request.session.session_key, user=request.user):
            return Response({'message': 'User is not logged into Spotify.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            wrapped = create_wrapped(request.user, term)
            return Response({'id': wrapped}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Failed to wrap'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, format=None):
        try:
            wraps = get_all_user_wraps(request.user)
            resp = WrappedSerializer(wraps, many=True, context={'request': request})
            return Response({'wraps': resp.data}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Failed to get wraps'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# probably not needed in final app version
class SingleWrapped(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request, id, format=None):
        try:
            wrap = get_wrap_by_id(request.user, id)
            resp = WrappedSerializer(wrap, context={'request': request})
            return Response(resp.data, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Failed to wrap'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfilePicture(APIView):
    authentication_classes = [SessionAuthentication]

    def get(self, request, format=None):
        if not is_spotify_authenticated(session_id=request.session.session_key, user=request.user):
            return Response({'message': 'User is not logged into Spotify.'}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            response = spotify_request(request.user, 'me')
            image = response['images'][0]['url']
            return Response({'url': image}, status=status.HTTP_200_OK)
        except:
            return Response({'message': 'Failed to get profile picture'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
