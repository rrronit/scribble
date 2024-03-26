from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Post,Like,Comment,SavePost
from supabase import create_client
import base64
from django.http import JsonResponse
from .models import Post, Like
from django.shortcuts import get_object_or_404
import uuid
import json

supabaseUrl = "https://dnltmfhvtgzozvroiwor.supabase.co"
supabasekey="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRubHRtZmh2dGd6b3p2cm9pd29yIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNzMxNzQ0NCwiZXhwIjoyMDIyODkzNDQ0fQ.UeEyCm9MCEheJ9ZElyJoX1ywcdXEJvv3jhH6n8QvZ4E"
supabase=create_client(supabaseUrl,supabasekey)

def index(req):
    user=req.user
    print(user)
    if user.is_authenticated:
        posts=Post.objects.all()

        #Get like status each post
        for post in posts:
            post.is_liked = Like.objects.filter(post=post, user=user).exists()
        params={"posts":posts}
        return render(req,"homepage.html",params)
    return render(req,"account/login.html")
    


@csrf_exempt
def createPost(req):
    user=User.objects.all()[0]
    image=req.body
    image=image.decode("utf-8")
    base64_image = image.split(',')[1]
    binary_image = base64.b64decode(base64_image)
    storage = supabase.storage.from_("scribble")
    file_name=str(uuid.uuid4())
    file_path="Post/"+file_name+".jpg"
    storage.upload(file=binary_image,path=file_path,file_options={"content-type":"image/jpeg"})
    newPost=Post(user=user,image_url=storage.get_public_url(file_path))
    newPost.save()
    return HttpResponse("done")


def deletePost(req):
    user=req.user
    imageId=req.imageId
    
    imageToDelete=Post.objects.get(id=imageId)
    if imageToDelete.user==user:
        
        imageToDelete.delete()
        return HttpResponse("done")
    
    return HttpResponse("not allowed",status=404)


@csrf_exempt
def likeImage(req):
    if req.method == 'POST':
        user = req.user
        data = json.loads(req.body)
        img_id =data['imgId']  
     
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
    
    
    
    
def addComment(req):
    if req.method == 'POST':
        user = req.user
        post_id = req.POST.get('postId') 
        content = req.POST.get('content')  
        
        post = get_object_or_404(Post, pk=post_id)
        
        comment = Comment.objects.create(post=post, user=user, content=content)
        
        comment_data = {
            'id': comment.id,
            'user': comment.user.username,
            'content': comment.content,
            'created_at': comment.created_at.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return JsonResponse({'status': 'success', 'comment': comment_data})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    
    
def savePost(request):
    if request.method == 'POST':
        user = request.user
        post_id = request.POST.get('postId') 
        
        post = get_object_or_404(Post, pk=post_id)
        
        if SavePost.objects.filter(post=post, user=user).exists():
            return JsonResponse({'error': 'Post already saved'}, status=400)
        else:
            save_post = SavePost.objects.create(post=post, user=user)
            return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    
from django.db.models import Q

@csrf_exempt
def searchUser(req):
    userToSearch=json.loads(req.body)["user"]
    print(userToSearch)
    users = list(User.objects.filter(Q(username__contains=userToSearch) | Q(email__contains=userToSearch)).values())
    
    params = {
        'users': users
    }

    
    return JsonResponse(params)