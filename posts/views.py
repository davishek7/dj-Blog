from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404,redirect,reverse
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponse
from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from .models import Post, Comment,Category
from .forms import NewCommentForm, PostForm, SearchForm,CategoryForm,SubscribeForm
from django.core.paginator import Paginator ,EmptyPage,PageNotAnInteger
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountMixin
from django.contrib.postgres.search import SearchVector,SearchQuery,SearchRank
from django.contrib import messages


class PostList(ListView):
    model=Post
    template_name='posts/index.html'
    context_object_name='posts'
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context

    def get_queryset(self):
        return Post.objects.filter(status='published')


def post_detail(request,slug):
    post=get_object_or_404(Post,slug=slug,status='published')

    allcomments=post.comments.filter(status=True)
    page=request.GET.get('page',1)
    paginator= Paginator(allcomments,3)

    context={}

    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(post)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted'] = hit_count_response.hit_counted
        hitcontext['hit_message'] = hit_count_response.hit_message
        hitcontext['total_hits'] = hits

    user_comment=None

    if request.method=='POST':
        comment_form=NewCommentForm(request.POST)
        if comment_form.is_valid():
            user_comment=comment_form.save(commit=False)
            user_comment.post=post
            user_comment.save()
            return HttpResponseRedirect('/posts/'+post.slug)
    else:
        comment_form = NewCommentForm()
    context = {'post': post, 'comment_form': comment_form,'allcomments':allcomments,
               'comments': user_comment,'title': post.title}
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

def category_list(request,category_slug):
    category=get_object_or_404(Category,slug=category_slug)
    posts=Post.objects.filter(category=category)
    context={'category':category,'posts':posts,'title':category.name}
    return render(request,'posts/category.html',context)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class=CategoryForm
    success_url = reverse_lazy('posts:all-posts')

    def form_valid(self,form):
        form.instance.slug = slugify(form.instance.name)
        return super(CategoryCreateView,self).form_valid(form)


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
    message = {}
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