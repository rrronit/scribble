from django.shortcuts import render
from django.contrib.auth.models import User
from post.models import Post

# Create your views here.
def explore(req):
    user=req.user
    print(user)
    if user.is_authenticated:
        random_posts = Post.objects.order_by('?')[:9]  
        context = {
        'posts': random_posts
        }
        return render(req, 'explore/explore.html', context)
    return render(req,"index.html")

def trending(req):
    user=req.user
    print(user)
    if user.is_authenticated:
        random_posts = Post.objects.order_by('?')[:10]  
        context = {
        'posts': random_posts
        }
        return render(req, 'explore/trending.html', context)
    return render(req,"index.html")