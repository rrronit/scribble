
from django.urls import path  
from .views import *
from . import views

urlpatterns = [
    path('', index ),
    path("createPost/",createPost),
    path("deletepost",deletePost),
    path('add-comment', addComment),
    path('like-image', likeImage),
    path('save-post', savePost),
    path("search-user",searchUser)
   
]

