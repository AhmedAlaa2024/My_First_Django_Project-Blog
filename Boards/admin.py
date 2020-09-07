from django.contrib import admin
from .models import Board, Topic, Post

# Register your models here.
@admin.register(Board)
@admin.register(Topic)
@admin.register(Post)
class AuthorAdmin(admin.ModelAdmin):
    pass