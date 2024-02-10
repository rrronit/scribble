
from django.urls import path  
from .views import *

urlpatterns = [
    path('', index ),
    path("createPost/",createPost),
    path("deletepost",deletePost)
]

