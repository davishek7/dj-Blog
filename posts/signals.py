import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string,get_template
from posts.models import Post,Subscribe


@receiver(post_save, sender=Post)
def subscribe_email(sender, instance, created, **kwargs):

    if settings.DEBUG:
        url = 'http://' + settings.ALLOWED_HOSTS[0] + f':8000/posts/{instance.slug}'
    else:
        url = 'https://' + settings.ALLOWED_HOSTS[1] + f'/posts/{instance.slug}'

    msg_html = get_template('posts/subscriber_email.html').render({
        'url':url,
        'instance':instance
    })

    if created and instance.status == 'published':
        send_mail(
            'New Post',
            f'{instance.title} has been posted',
            "avishekdjangoblog admin <os.environ.get('EMAIL_USER')>",
            list(Subscribe.objects.all()),
            html_message=msg_html,
            fail_silently=False,

        )