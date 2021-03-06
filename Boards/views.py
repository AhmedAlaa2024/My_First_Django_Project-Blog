from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, Http404, HttpRequest
from django.contrib.auth.models import User
from .models import Board, Topic, Post
from .forms import NewTopicForm, NewPostForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.views.generic import UpdateView, ListView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# Create your views here.

'''
def home(request):
    boards = Board.objects.all().order_by('-created_dt')
    return render(request, 'home.html', {'boards': boards})
'''

class BoardListView(ListView):
    model = Board
    context_object_name = 'boards'
    template_name = 'home.html'


def board_topics(request, board_name):
    # A method to get Error404 Not Found Page using Python3's basics.
    # try:
    #    board = Board.objects.get(name=board_name)
    # except Board.DoesNotExist:
    #    raise Http404

    # A method to get Error404 Page Not Found using django shourtcuts
    # Note: you should import get_object_or_404 from django.shortcuts
    board = get_object_or_404(Board, name=board_name)
    queryset = board.topics.order_by('-created_dt').annotate(comments=Count('posts'))
    page = request.GET.get('page', 1)
    paginator = Paginator(queryset, 20)
    try:
        topics = paginator.page(page)
    except PageNotAnInteger:
        topics = paginator.page(1)
    except EmptyPage:
        topics = paginator.page(paginator.num_pages)
    return render(request, 'topics.html', {'board': board, 'topics': topics})

@login_required
def new_topic(request, board_name):
    board = get_object_or_404(Board, name=board_name)
    if request.method == "POST":
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.created_by = request.user
            topic.save()
            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                created_by=request.user,
                topic=topic
            )
            return redirect('board_topics', board_name=board.name)
    else:
        form = NewTopicForm()
    return render(request, 'new_topic.html', {'board': board, 'form': form})

def topic_posts(request, board_name, topic_subject):
    topic = get_object_or_404(Topic, board__name=board_name, subject=topic_subject)
    posts = topic.posts.all().order_by('-created_dt')
    session_key = 'view_topic_{}'.format(topic.pk)
    if not request.session.get(session_key, False):
        topic.views += 1
        topic.save()
        request.session[session_key] = True
    return render(request, 'topic_posts.html', {'topic': topic, 'posts': posts})

@login_required
def reply_topic(request, board_name, topic_subject):
    board = get_object_or_404(Board, name=board_name)
    topic = get_object_or_404(Topic, board__name=board_name, subject=topic_subject)
    if request.method == "POST":
        form = NewPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.updated_by = request.user
            topic.updated_dt = timezone.now()
            topic.save()
            return redirect('topic_posts', board_name=board.name, topic_subject=topic.subject)
    else:
        form = NewPostForm()
    return render(request, 'reply_topic.html', {'topic': topic, 'form': form})

@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ['message']
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.updated_dt = timezone.now()
        post.save()
        return redirect('topic_posts', board_name=post.topic.board.name, topic_subject=post.topic.subject)