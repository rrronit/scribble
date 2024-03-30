from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Post,Like,Comment,SavePost
from supabase import create_client
import base64
from django.http import JsonResponse
from .models import Post, Like,Comment
from account.models import Profile
from django.shortcuts import get_object_or_404
import uuid
import json
import random
import os
from django.contrib.auth.decorators import login_required


supabaseUrl = os.getenv('supabaseUrl')
supabasekey=os.getenv('supabasekey')
supabase=create_client(supabaseUrl,supabasekey)

@login_required
def index(req):
    user=req.user
    if user.is_authenticated:
        posts=Post.objects.all()
        all_users = User.objects.all()
        suggestions = random.sample(list(all_users), min(len(all_users),8))
        
        
        for post in posts:
            post.is_liked = Like.objects.filter(post=post, user=user).exists()
            post.profile_url=Profile.objects.get(user=post.user).profileimg
            post.is_saved = SavePost.objects.filter(post=post, user=user).exists()
            post.save_count = len(SavePost.objects.filter(post=post))
            post.comment_count=len(Comment.objects.filter(post=post))
                
        for suggestion in suggestions:
            suggestion.profile_url=Profile.objects.get(user=suggestion).profileimg
            
       
        params = {
            "posts": posts,
            "suggestions": suggestions
        }
        return render(req,"homepage.html",params)
    return render(req,"account/login.html")
    

@login_required
@csrf_exempt
def createPost(req):
    user=req.user
    data=json.loads(req.body)
    image=data["image"]
    content=data["caption"]
    base64_image = image.split(',')[1]
    binary_image = base64.b64decode(base64_image)   
    storage = supabase.storage.from_("scribble")
    file_name=str(uuid.uuid4())
    file_path="Post/"+file_name+".jpg"
    storage.upload(file=binary_image,path=file_path,file_options={"content-type":"image/jpeg"})
    newPost=Post(user=user,image_url=storage.get_public_url(file_path),content=content)
    newPost.save()
    return HttpResponse("done")

@login_required
def deletePost(req):
    user=req.user
    imageId=req.imageId
    
    imageToDelete=Post.objects.get(id=imageId)
    if imageToDelete.user==user:
        
        imageToDelete.delete()
        return HttpResponse("done")
    
    return HttpResponse("not allowed",status=404)

@login_required
@csrf_exempt
def likeImage(req):
    if req.method == 'POST':
        user = req.user
        data = json.loads(req.body)
        print("#############################",data)
        img_id =data['imgId'] 
        print(img_id) 
        
        post = get_object_or_404(Post, pk=img_id)
        
        if post:
            like_exists = Like.objects.filter(post=post, user=user).exists()
           
            
            if like_exists:
                img=Like.objects.filter(post=post, user=user).delete()
                post.like_count -= 1
                post.save()
                print(post.like_count)
                
                return JsonResponse({'status': 'unliked'})
            else:
                img=Like.objects.create(post=post, user=user)
                post.like_count += 1
                post.save()
                print(post.like_count)
                
                return JsonResponse({'status': 'liked'})
        else:
            return JsonResponse({'error': 'Post does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    
from django.core import serializers
@login_required
def showComment(request, id):
    post = get_object_or_404(Post, pk=id)
    comments = Comment.objects.filter(post=post)
    # Add username field to each comment
    comment_data = []
    for comment in comments:
        comment_dict = {
            'username': comment.user.username, 
            'content': comment.content,
            'created_at': comment.created_at
        }
        comment_data.append(comment_dict)
    return JsonResponse({'comments': comment_data})
    
@login_required
@csrf_exempt    
def addComment(req):
    if req.method == 'POST':
        user = req.user
        data = json.loads(req.body)
        post_id =data['postId']   
        content =data['content']   
        
        post = get_object_or_404(Post, pk=post_id)
        
        comment = Comment.objects.create(post=post, user=user, content=content)

        
        comment_data = {
            'id': comment.id,
            'user': comment.user.username,
            'content': comment.content,
        }
        comment.save()
        
        return JsonResponse({'status': 'success', 'comment': comment_data})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@login_required
@csrf_exempt
def savePost(req):
    if req.method == 'POST':
        user = req.user
        data = json.loads(req.body)
        print("--------------------------------------------",data)
        save_Id =data['saveId']  
        post = get_object_or_404(Post, pk=save_Id)

        if SavePost.objects.filter(post=post, user=user).exists():
            save_post = SavePost.objects.filter(post=post, user=user).delete()
            post.save()
            return JsonResponse({'status': 'unsaved'})
        else:
            save_post = SavePost.objects.create(post=post, user=user)
            post.save()
            return JsonResponse({'status': 'saved'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    
from django.db.models import Q,F


@login_required
@csrf_exempt
def searchUser(req):
    userToSearch=json.loads(req.body)["user"]
 
    users = User.objects.filter(Q(username__contains=userToSearch) | Q(email__contains=userToSearch))
    users = users.annotate(profile_url=F('profile__profileimg'))
   
    users=list(users.values())
    params = {
        'users': users
    }

    
    return JsonResponse(params)