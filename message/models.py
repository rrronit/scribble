from django.db import models
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField()

    def __str__(self):
        return f'{self.user.username}  {self.timestamp}: {self.content}'



