from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import CommentForm, PostForm, SearchForm,CategoryForm
from django.core.paginator import Paginator ,EmptyPage,PageNotAnInteger
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin, HitCountDetailView
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from django.contrib import messages


class PostList(ListView):
    model=Post
    template_name='frontend/index.html'
    context_object_name='posts'
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context

    def get_queryset(self):
        return Post.objects.select_related('category').filter(status='published')


class PostDetailView(HitCountDetailView,FormMixin):
    model = Post
    count_hit = True
    template_name = 'posts/post.html'
    context_object_name = 'post'
    form_class = CommentForm

    def get_success_url(self):
        return reverse('posts:post-detail', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            form.instance.post = self.object
            form.save()
            messages.success(request,'Thanks for your feedback.')
            return self.form_valid(form)
        else:
            messages.warning(self.request,'Something went wrong!')
            return self.form_invalid(form)

    def form_valid(self, form):
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comment_form"] = self.get_form()
        context["tags"] = context["post"].tags.all()
        context["comments"] = context["post"].comments.select_related('post').filter(status = True).order_by('-created')
        return context


class PostCreateView(LoginRequiredMixin,CreateView):
    model=Post
    form_class=PostForm
    success_url=reverse_lazy('posts:all-posts')

    def form_valid(self,form):
        form.instance.author=self.request.user
        form.instance.slug = slugify(form.instance.title)
        messages.success(self.request, f'{form.instance.title} created successfully')
        return super(PostCreateView,self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create a New Blogpost'
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin,UpdateView):
    model=Post
    form_class = PostForm
    success_url = reverse_lazy('accounts:dashboard')

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
    success_url = reverse_lazy('accounts:dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete a Blogpost'
        return context

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['status']
    success_url = reverse_lazy('accounts:dashboard')

    def form_valid(self, form):
        form.instance.post = self.post
        return super(CommentUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update a Blog Comment'
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'posts/category.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(category__slug = self.object.slug)
        return context


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class=CategoryForm
    success_url = reverse_lazy('posts:all-posts')

    def form_valid(self,form):
        form.instance.slug = slugify(form.instance.name)
        return super(CategoryCreateView,self).form_valid(form)


class TagDetailView(DetailView):
    model = Tag
    template_name = 'posts/tag.html'
    context_object_name = 'tag'

    def get_context_data(self, **kwargs):
        self.object = self.get_object()
        context = super().get_context_data(**kwargs)
        context["posts"] = Post.objects.filter(tags__slug = self.object.slug)
        return context
        

def search(request):
    form = SearchForm()
    q=''
    results = []

    if 'q' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            q=form.cleaned_data['q']

            vector = SearchVector('title',weight='A')+\
                SearchVector('content',weight='B')

            query = SearchQuery(q)

            results = Post.objects.annotate(rank=SearchRank(vector,query,cover_density=True)).order_by('-rank')

            results = Post.objects.annotate(
                search=SearchVector('title','content',),).filter(search=SearchQuery(q))

    context = {'form': form, 'q': q, 'results':results}
    return render(request, 'posts/search.html', context)


def about(request):
    return render(request,'posts/about.html')


def subscribe(request):
    if request.method == 'POST':
        form = SubscribeForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Thank you for subscribing!')
        else:
            messages.warning(request,form.errors['email'])
    else:
        messages.warning(request,'Your are not allowed to view this page')
        return redirect('/')
    return render(request,'posts/subscribe_status.html')
