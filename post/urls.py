
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
    path("get_comment/<int:id>",showComment),
    path("search-user",searchUser)
   
]

