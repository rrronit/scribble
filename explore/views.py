from django.shortcuts import render
from django.contrib.auth.models import User
from post.models import Post
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from supabase import create_client
import base64
from django.http import JsonResponse
from post.models import Post,Like,Comment,SavePost
from django.shortcuts import get_object_or_404
import json

def index(req):
    user=req.user
    print(user)
    if user.is_authenticated:
        posts=Post.objects.all()

        #Get like status each post
        for post in posts:
            post.is_liked = Like.objects.filter(post=post, user=user).exists()
            post.is_saved = SavePost.objects.filter(post=post, user=user).exists()
            post.save_count = len(SavePost.objects.filter(post=post))
            post.comment_count=len(Comment.objects.filter(post=post))
        params={"posts":posts}
        return render(req,"explore.html",params)
    return render(req,"account/login.html")



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



    
