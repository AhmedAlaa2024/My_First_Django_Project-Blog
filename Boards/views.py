from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpRequest
from django.contrib.auth.models import User
from .models import Board, Topic, Post
from .forms import NewTopicForm

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
    user = User.objects.first()
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                created_by=user,
                topic=topic
            )
            return redirect('board_topics', board_name=board.name)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})
