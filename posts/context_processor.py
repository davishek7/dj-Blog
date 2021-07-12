from .models import Post, Comment,Category
from .forms import SubscribeForm


def categories(request):
    return {
        'categories':Category.objects.all()
    }

def sidebar_comments(request):
    return {
        'sidebar_comments': Comment.objects.filter(status=True)[:5]
    }
def sidebar_posts(request):
    return{
        'sidebar_posts':Post.objects.filter(status='published')[:5]
    }

def subscribe_form(request):
    return{
        'subscribe_form':SubscribeForm()
    }