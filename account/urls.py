from django.urls import path  
from .views import *
urlpatterns = [
     path('register/',register),
    path('login/',login),
    path('logout/',logout),
    path('verification/',verify_otp),
    path('profile/<str:id_user>',profile),
    path('follow',follow),
    path('edit/<str:id_user>',edit),

]