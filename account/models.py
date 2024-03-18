from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    profile_id = models.IntegerField(primary_key=True)
    profile_url = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)
    user_id = models.IntegerField()


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
