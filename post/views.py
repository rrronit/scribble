from django.shortcuts import render
from django.contrib.auth.models import User


def index(req):
    User.objects({})
    return render(req,"index.html")


def createPost(req):
    return render(req,"post-scribble/dist/index.html")