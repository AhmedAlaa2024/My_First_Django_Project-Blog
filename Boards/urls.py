from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('boards/<board_name>/', views.board_topics, name='board_topics'),
    path('boards/<board_name>/new/', views.new_topic, name='new_topic'),
]

