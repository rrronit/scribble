from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.AutoField(primary_key=True, )
    bio = models.TextField(blank=True, default='')
    profileimg = models.URLField(default="https://i.pinimg.com/564x/c0/27/be/c027bec07c2dc08b9df60921dfd539bd.jpg")
    location = models.CharField(max_length=100, blank=True, default='')
    

    def __str__(self):
        return self.user.username
 


# class Follow(models.Model):
#     follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
#     following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')

class Followers(models.Model):
    follower = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user