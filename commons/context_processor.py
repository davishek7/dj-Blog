from django.contrib.auth.models import User
from posts.models import Post, Comment,Category
from posts.forms import SearchForm


def global_context(request):

    return {
        'user':User.objects.first(),
        'categories':Category.objects.all(),
        'sidebar_comments': Comment.objects.filter(status=True)[:5],
        'sidebar_posts':Post.objects.filter(status='published')[:5],
        'search_form':SearchForm(),
        # 'subscribe_form':SubscribeForm(),
        # 'notifications':Notification.objects.filter(status__in = [0,1])[:10],
        # 'count':Notification.objects.filter(status = 1).all().count()
    }
