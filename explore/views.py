from django.shortcuts import render
from django.contrib.auth.models import User
from post.models import Post
from account.models import Profile
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from post.models import Post,Like,Comment,SavePost
from post.models import SavePost, Like


def explore(req):
    user=req.user
    print(user)
    if user.is_authenticated:
        random_posts = Post.objects.order_by('?')[:12]  
       
        for post in random_posts:
            post.is_liked = Like.objects.filter(post=post, user=user).exists()
            post.is_saved = SavePost.objects.filter(post=post, user=user).exists()
            post.save_count = len(SavePost.objects.filter(post=post))
            post.profile_url=Profile.objects.filter(user=post.user)[0].profileimg 
            post.comment_count=len(Comment.objects.filter(post=post))
        params={"posts":random_posts}
        return render(req, 'explore/explore.html',params)
    return render(req,"index.html")

def trending(req):
   user=req.user
   if user.is_authenticated:
        random_posts = Post.objects.order_by('?')[:12]  
       
        for post in random_posts:
            post.is_liked = Like.objects.filter(post=post, user=user).exists()
            post.is_saved = SavePost.objects.filter(post=post, user=user).exists()
            post.save_count = len(SavePost.objects.filter(post=post))
            post.profile_url=Profile.objects.filter(user=post.user)[0].profileimg 
            post.comment_count=len(Comment.objects.filter(post=post))
        params={"posts":random_posts}
        return render(req, 'explore/trending.html',params)
   return render(req,"index.html")



def savePost(req):
     user=req.user
     if user.is_authenticated:
        random_posts = SavePost.objects.filter(user=req.user)  
       
        for post in random_posts:
            post.is_liked = Like.objects.filter(post=post.post, user=user).exists()
            post.is_saved = SavePost.objects.filter(post=post.post, user=user).exists()
            post.save_count = len(SavePost.objects.filter(post=post.post))
            post.profile_url=Profile.objects.filter(user=post.post.user)[0].profileimg 
            post.comment_count=len(Comment.objects.filter(post=post.post))
        params={"posts":random_posts}
        return render(req, 'explore/savedPost.html',params)
     return render(req,"index.html")

def likedPost(req):
     user=req.user
     if user.is_authenticated:
        random_posts = Like.objects.filter(user=req.user)  
       
        for post in random_posts:
            post.is_liked = Like.objects.filter(post=post.post, user=user).exists()
            post.is_saved = SavePost.objects.filter(post=post.post, user=user).exists()
            post.save_count = len(SavePost.objects.filter(post=post.post))
            post.profile_url=Profile.objects.filter(user=post.post.user)[0].profileimg 
            post.comment_count=len(Comment.objects.filter(post=post.post))
        params={"posts":random_posts}
        return render(req, 'explore/likedPost.html',params)
     return render(req,"index.html")

