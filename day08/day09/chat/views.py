from django.shortcuts import get_object_or_404, render
from .models import Room
from django.contrib.auth.decorators import login_required

# Create your views here.

def lobby(request):
    rooms = Room.objects.all() 
    return render(request, "chat/lobby.html", {'rooms': rooms})

@login_required(login_url='/account/')  
def room(request, room_name):
    get_object_or_404(Room, name=room_name)
    return render(request, "chat/room.html", {'room_name': room_name})