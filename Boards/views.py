from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpRequest
from django.contrib.auth.models import User
from .models import Board, Topic, Post

# Create your views here.


def home(request):
    boards = Board.objects.all()
    return render(request, 'home.html', {'boards': boards})


def board_topics(request, board_name):
    # A method to get Error404 Not Found Page using Python3's basics.
    # try:
    #    board = Board.objects.get(name=board_name)
    # except Board.DoesNotExist:
    #    raise Http404

    # A method to get Error404 Page Not Found using django shourtcuts
    # Note: you should import get_object_or_404 from django.shortcuts
    board = get_object_or_404(Board, name=board_name)
    return render(request, 'topics.html', {'board': board})


def new_topic(request, board_name):
    board = get_object_or_404(Board, name=board_name)
    if request.method == 'POST':
        subject = request.POST['subject']
        message = request.POST['message']
        user = User.objects.first()

        topic = Topic.objects.create(
            subject=subject,
            board=board,
            created_by=user
        )

        post = Post.objects.create(
            message=message,
            topic=topic,
            created_by=user
        )
        return redirect('board_topics', board_name=board.name)
    return render(request, 'new_topic.html', {'board': board})
