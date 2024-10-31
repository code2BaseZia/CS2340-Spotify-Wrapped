from django.db import models
from wrapped.models import Profile


class SpotifyToken(models.Model):
    session = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    refresh_token = models.CharField(max_length=150)
    access_token = models.CharField(max_length=150)
    expires_in = models.DateTimeField()
    token_type = models.CharField(max_length=50)


class SpotifyUserWrap(models.Model):
    THEME = {
        "no": "None",
        "ch": "Christmas",
        "hw": "Halloween",
        "ea": "Easter",
    }

    wrapped_id = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    theme = models.CharField(default="no", max_length=2, choices=THEME.items())
    # When the user who generated these wraps deletes their account, the on_delete will delete their wraps
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)