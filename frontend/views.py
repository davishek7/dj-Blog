from django.shortcuts import render
from posts.models import Post

# Create your views here.

def index(request):
    posts = Post.objects.select_related('category', 'author').order_by('-created').all()
    post = Post.objects.select_related('category', 'author').order_by('created').first()
    context = {'posts':posts, 'post':post}
    return render(request, 'frontend/index.html', context=context)