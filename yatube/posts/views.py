from typing import Text
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post, Group

# Create your views here.
def index(request):
    template = 'posts/index.html'
    posts = Post.objects.order_by('-pub_date')[:10]
    context = {
        'text':posts,
    }
    return render(request, template, context)

def group_list(request):
    template = 'posts/group_list.html'
    context = {
        'text':'Здесь будет информация о группах проекта Yatube',
    }
    return render(request, template, context)

def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    template = 'posts/group_posts.html'
    posts = Post.objects.filter(group=group).order_by('-pub_date')[:10]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)