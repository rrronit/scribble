from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default="") 
    image_url = models.URLField(null=True, blank=True)
    like_count=models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Post - {self.created_at}"
    
    
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user  = models.ForeignKey(User, on_delete = models.CASCADE)
    def _str_(self):
        return f"{self.post}'s Post - {self.User}"
   

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add = True)



class SavePost(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user  = models.ForeignKey(User, on_delete = models.CASCADE)
   


            