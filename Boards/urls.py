from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('boards/<board_name>/', views.board_topics, name='board_topics'),
    path('boards/<board_name>/new/', views.new_topic, name='new_topic'),
    path('boards/<board_name>/topics/<topic_subject>/',
         views.topic_posts, name='topic_posts'),
    path('boards/<board_name>/topics/<topic_subject>/reply/',
         views.reply_topic, name='reply_topic'),
]
