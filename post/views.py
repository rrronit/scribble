from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Post
from supabase import create_client
import base64
import uuid

supabaseUrl = "https://dnltmfhvtgzozvroiwor.supabase.co"
supabasekey="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRubHRtZmh2dGd6b3p2cm9pd29yIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNzMxNzQ0NCwiZXhwIjoyMDIyODkzNDQ0fQ.UeEyCm9MCEheJ9ZElyJoX1ywcdXEJvv3jhH6n8QvZ4E"
supabase=create_client(supabaseUrl,supabasekey)

def index(req):
    user=req.user
    print(user)
    if user.is_authenticated:
        posts=Post.objects.all()
        params={"posts":posts}
        return render(req,"homepage.html",params)
    return render(req,"index.html")
    


@csrf_exempt
def createPost(req):
    user=req.user
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





    
