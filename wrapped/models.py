from django.db.models.signals import post_save
from django.contrib.auth.models import User
from api.models import SpotifyToken
from django.db import models


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