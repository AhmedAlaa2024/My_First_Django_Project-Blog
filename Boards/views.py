from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from .models import Board

# Create your views here.

def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})

def board_topics(request, board_name):
    #A method to get Error404 Not Found Page using Python3's basics.
    #try:
    #    board = Board.objects.get(name=board_name)
    #except Board.DoesNotExist:
    #    raise Http404

    #A method to get Error404 Page Not Found using django shourtcuts
    #Note: you should import get_object_or_404 from django.shortcuts
    board = get_object_or_404(Board, name=board_name)

    return render(request, 'topics.html', {'board': board})