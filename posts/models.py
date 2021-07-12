from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


class Category(models.Model):
    name=models.CharField(max_length=200,db_index=True)
    slug=models.SlugField(max_length=200,unique=True)

    class Meta:
        verbose_name_plural = 'categories'
    
    def get_absolute_url(self):
        return reverse('posts:category_list',args=[self.slug])
    
    def __str__(self):
        return self.name

class Post(models.Model):

    options = (
        ('draft','Draft'),
        ('published','Published')
    )
    category=models.ForeignKey(Category,related_name='post',default=1,on_delete=models.SET_NULL,null=True,blank=True)
    title = models.CharField(max_length=200, blank=True, null=True,db_index=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    image = models.ImageField(default='thumbnail.png')
    published=models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    content = RichTextUploadingField(blank=True, null=True, db_index=True)
    status=models.CharField(max_length=10,choices=options,default='draft')

    class Meta:
        ordering=['-published']

    def get_absolute_url(self):
        return reverse('posts:post-detail', args=[self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,related_name='comments', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    status=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}'s comment on '{self.post}'"

    class Meta:
        ordering=['-created']


class Subscribe(models.Model):
    email = models.EmailField(max_length=254,blank=True,null=True)

    def __str__(self):
        return self.email
