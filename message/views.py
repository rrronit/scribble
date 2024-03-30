
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required()
def chat(request):
    messages = Message.objects.order_by('timestamp')
    return render(request, 'message/chat.html', {'messages': messages, 'user': request.user})
