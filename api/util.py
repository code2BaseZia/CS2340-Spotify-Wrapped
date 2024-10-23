from .models import SpotifyToken
from wrapped.models import Profile
from django.utils import timezone
from datetime import timedelta
from requests import post
import os


def get_user_tokens(session_id, user=None):
    if user is not None:
        profile = user.profile
        try:
            user_tokens = [profile.token]
        except:
            return None
    else:
        user_tokens = SpotifyToken.objects.filter(session=session_id)
        if not user_tokens.exists():
            return None
    return user_tokens[0]


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


def is_spotify_authenticated(session_id, user=None):
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
    refresh_token = response.get('refresh_token')

    # If this doesn't work, he changes the method to use session_id instead of passing in tokens
    update_or_create_user_tokens(tokens.sesson_id, access_token, token_type, expires_in, refresh_token, user)


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
