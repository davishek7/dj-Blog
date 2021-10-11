from .models import Post, Comment,Category,Notification
from .forms import SubscribeForm


def global_context(request):

    return {
        'categories':Category.objects.all(),
        'sidebar_comments': Comment.objects.filter(status=True)[:5],
        'sidebar_posts':Post.objects.filter(status='published')[:5],
        'subscribe_form':SubscribeForm(),
        'notifications':Notification.objects.filter(status__in = [0,1])[:10],
        'count':Notification.objects.filter(status = 1).all().count()
    }
