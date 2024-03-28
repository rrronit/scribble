from django.urls import path  
from .views import *
urlpatterns = [
     path('explore/',explore),
    path('trending/',trending),
    path('savedPost/',savePost),
    path('likedPost/',likedPost),
   
    
]