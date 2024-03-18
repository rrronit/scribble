
from django.urls import path  
from .views import *
from . import views

urlpatterns = [
    path('', index ),
    path("createPost/",createPost),
    path("deletepost",deletePost),
   
]

