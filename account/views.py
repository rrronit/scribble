from django.shortcuts import render
from django.shortcuts import render,HttpResponse,redirect
import json
from django.contrib.auth.models import User 
from django.contrib import auth
import re
import random
import redis
from django.core.mail import send_mail
import os
import threading
from supabase import create_client
import base64
import uuid

supabaseUrl = "https://dnltmfhvtgzozvroiwor.supabase.co"
supabasekey="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRubHRtZmh2dGd6b3p2cm9pd29yIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwNzMxNzQ0NCwiZXhwIjoyMDIyODkzNDQ0fQ.UeEyCm9MCEheJ9ZElyJoX1ywcdXEJvv3jhH6n8QvZ4E"
supabase=create_client(supabaseUrl,supabasekey)


r = redis.Redis(
  host=os.getenv('REDIS_HOST'),
  ssl=True,
  port=40073,
  password=os.getenv('REDIS_PASSWORD'),
)


def generate_otp():
   return random.randint(1000,9999)


def send_otp_email(email,otp):
  subject = 'OTP Verification'
  message = f'Your OTP is: {otp}\nExpire in 5min '
  from_email = 'test.mail240723@gmail.com'
  recipient_list = [email]
  send_mail(subject, message,from_email,recipient_list)


def verify_otp(req):
    if req.method == 'POST':

      user_otp=req.POST['user_otp']

      email=req.session.get('user_data')['email']
      redis_key = f'otp:{email}'
      stored_otp = r.get(redis_key)
      user_data = req.session.get('user_data')
      
      if stored_otp!=None and int(stored_otp) == int(user_otp):
         if user_data:
                user = User(username=user_data['username'], email=user_data['email'])
                profile=Profile(user=user)
                user.set_password(user_data['password'])
                user.save()
                profile.save()
                auth.login(req,user)
                del req.session['user_data']
               
                return redirect('/')
      else:
        params={'email':user_data['email'],'error':"Incorrect OTP"}
        
        return render(req,'account/verification.html',params)   
    user=req.session.get('user_data')
    if user:
      print(user)
      params={'email':user['email']}
      return render(req,'account/verification.html',params)
      
    return redirect("/register")


def register(req):
    user=req.user
    if user.is_authenticated:
       return redirect("/")
    if req.method =='POST':
       username=req.POST['f_name']
       email=req.POST['mail'].lower()
       password=req.POST['pass']
       

       if len(username)<3 or len(username)>25:
          req.session['error']="Invalid username"
          return redirect("/register")
       
       regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
       if not (re.fullmatch(regex,email)):
           req.session['error']="Incorrect email"
           return redirect("/register")
       
       if  len(password)<8:
          req.session['error']="Invalid Password"
          return redirect("/register")  
       
       if User.objects.filter(username=username).exists():
          req.session['error']="Username already taken"
          return redirect("/register")
       
       if User.objects.filter(email=email).exists():
          req.session['error']="Email already taken"
          return redirect("/register")
       
       otp = generate_otp()
       print(otp)
       redis_key = f'otp:{email}'
       r.set(redis_key, otp, ex=300)
       print(redis_key)

       #send_otp_email(email, otp)
       threading.Thread(target=send_otp_email, args=(email, otp)).start()
      
       req.session['user_data'] = {
            'username': username,
            'email': email,
            'password': password,
        }       
       response=redirect('/verification')
       print('dsfsfs')
       return response
    else:
     
     error=req.session.get("error","")
     req.session['error']=''
     return render(req,'account/register.html',{"error":error})


def login(req):
    user=req.user
    if user.is_authenticated:
       return redirect("/")
    if req.method =='POST':
       
       
       email=req.POST['email'].lower()
       password=req.POST['password']
    

       regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
       if not (re.fullmatch(regex,email)):
           req.session['error']="Invalid Credentials"
           return redirect("/login")
       
       elif  len(password)<8:
          req.session['error']="Invalid Credentials"
          return redirect("/login")
      
       u=User.objects.filter(email=email)
       if u:
          username=u[0].username
          user=auth.authenticate(username=username,password=password)  
          if user is not None:
                auth.login(req,user)
                response=redirect('/')
                return response
          else:
                req.session['error']="Invalid Credentials"
                return redirect("/login")
       else:
            req.session['error'] = "Email does not exist."
            return redirect("/login")  
    
    else:
     error=req.session.get("error","")
     req.session['error']=''
     return render(req,'account/login.html',{"error":error})

def logout(req):
   auth.logout(req)
   
   return redirect("/")


from .models import Profile 
from post.models import Post

def profile(request,id_user):
   
    user_object = User.objects.get(username=id_user)
 
    profile = Profile.objects.get(user=user_object)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=user_object).order_by('-created_at')
    user_post_length = len(user_posts)


    follower = request.user.username
    user = id_user
    
    if Followers.objects.filter(follower=follower, user=user).first():
        follow_unfollow = 'Unfollow'
    else:
        follow_unfollow = 'Follow'

    user_followers = len(Followers.objects.filter(user=id_user))
    user_following = len(Followers.objects.filter(follower=id_user))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'profile': profile,
        'follow_unfollow':follow_unfollow,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    
    
   
    return render(request, 'profile.html', context)

from .models import Followers

def edit(request,id_user):
    
    if request.user.username == id_user:
        
        user_object = User.objects.get(username=id_user)

      
        profile = Profile.objects.get(user=user_object)
        user_profile = Profile.objects.get(user=user_object)
        if request.method == 'POST':
         
            image = request.FILES.get("image")
            if image:
                
               image=base64.b64encode(image.read())
         
               binary_image = base64.b64decode(image)
               storage = supabase.storage.from_("scribble")
               file_name=str(uuid.uuid4())
               file_path="Profile/"+file_name+".jpg"
               storage.upload(file=binary_image,path=file_path,file_options={"content-type":"image/jpeg"})
               user_profile.profileimg = storage.get_public_url(file_path)

            bio = request.POST['bio']
            location = request.POST['location']

            print(user_profile.profileimg)
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
            return redirect( '/profile/'+id_user)


        else:
            return render(request, 'profile.html') 


def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Followers.objects.filter(follower=follower, user=user).first():
            delete_follower = Followers.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = Followers.objects.create(follower=follower, user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')