from django.shortcuts import render



def index(req):
    
    return render(req,"index.html")


def createPost(req):
    return render(req,"post-scribble/dist/index.html")