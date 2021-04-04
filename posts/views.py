from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Comment,Category
from .forms import NewCommentForm,PostForm

def categories(request):
    return {
        'categories':Category.objects.all(),
    }

class PostList(ListView):
    model=Post
    template_name='posts/index.html'
    context_object_name='posts'
    paginate_by=5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context

    def get_queryset(self):
        return Post.objects.filter(status='published')


def post_detail(request,slug):
    post=get_object_or_404(Post,slug=slug,status='published')

    comments=post.comments.filter(status=True)

    user_comment=None

    if request.method=='POST':
        comment_form=NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment=comment_form.save(commit=False)
            user_comment.post=post
            user_comment.user=request.user
            user_comment.save()
            return HttpResponseRedirect('/posts/'+post.slug)
    else:
        comment_form = NewCommentForm()
    context={'post':post,'comment_form':comment_form,'comments':comments,'title':post.title}
    return render(request,'posts/post.html',context)


class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    form_class=PostForm
    success_url=reverse_lazy('posts:all-posts')

    def form_valid(self,form):
        form.instance.author=self.request.user
        form.instance.slug = slugify(form.instance.title)
        return super(PostCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a New Blogpost'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model=Post
    form_class = PostForm
    success_url = reverse_lazy('accounts:user-profile')

    def form_valid(self,form):
        form.instance.user=self.request.user
        return super(PostUpdateView,self).form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update a Blogpost'
        return context

    
    def test_func(self):
        post=self.get_object()
        if self.request.user==post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin,DeleteView):
    model=Post
    context_object_name='post'
    success_url = reverse_lazy('accounts:user-profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete a Blogpost'
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['body', 'status']
    success_url = reverse_lazy('accounts:user-profile')

    def form_valid(self, form):
        form.instance.post = self.post
        return super(CommentUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update a Blog Comment'
        return context

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    context_object_name = 'comment'
    success_url = reverse_lazy('accounts:user-profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete a Blog Comment'
        return context

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.user:
            return True
        return False

def category_list(request,category_slug):
    category=get_object_or_404(Category,slug=category_slug)
    posts=Post.objects.filter(category=category)
    context={'category':category,'posts':posts,'title':category.name}
    return render(request,'posts/category.html',context)


def about(request):
    return render(request,'posts/about.html')
