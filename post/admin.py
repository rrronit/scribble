from django.contrib import admin

# Register your models here.
from .models import Post, SavePost,Comment

admin.site.register(Post)
admin.site.register(SavePost)
admin.site.register(Comment)