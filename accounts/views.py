from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateUserForm,ProfileUpdateForm,UserUpdateForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import Profile
from posts.models import Post,Comment

def site_user(request):
	return{
		'user':User.objects.first()
	}

class UserLoginView(LoginView):
	template_name = 'accounts/login.html'

	def form_valid(self,form):
		login(self.request,form.get_user())
		return super(UserLoginView,self).form_valid(form)

	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['title']='Login'
		return context

class RegisterPage(FormView):
	template_name = 'accounts/register.html'
	form_class = CreateUserForm
	success_url = reverse_lazy('posts:all-posts')

	def form_valid(self, form):
		user = form.save()
		if user is not None:
			login(self.request, user)
		return super(RegisterPage, self).form_valid(form)
	
	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		context['title']='Register'
		return context

	def get(self, *args, **kwargs):
		if self.request.user.is_authenticated:
			return redirect('posts:all-posts')
		return super(RegisterPage, self).get(*args, **kwargs)

@login_required
def dashboard(request):
	posts=Post.objects.all()

	all_posts=posts.count()
	drafts=posts.filter(status='draft').count()
	published = posts.filter(status='published').count()

	page=request.GET.get('page',1)
	paginator=Paginator(posts,5)

	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		posts=paginator.page(1)
	except EmptyPage:
		posts=paginator.page(paginator.num_pages)

	if request.method == 'POST':
		u_form=UserUpdateForm(request.POST,instance=request.user)
		p_form = ProfileUpdateForm(
			request.POST, request.FILES, instance=request.user.profile)

		if u_form.is_valid() and p_form.is_valid():
			u_form.save()
			p_form.save()
			messages.success(request,'Your account has been updated')
			return redirect('accounts:dashboard')
	else:
		u_form = UserUpdateForm(instance=request.user)
		p_form = ProfileUpdateForm(instance=request.user.profile)

	context={'title':f"{request.user}'s Profile",'u_form':u_form,'p_form':p_form,'posts':posts,'all_posts':all_posts,'drafts':drafts,'published':published}
	return render(request,'accounts/dashboard.html',context)

class UserPostView(ListView):
	template_name='accounts/user_posts_edit.html'
	context_object_name='posts'
	paginate_by=10

	def get_queryset(self):
		return Post.objects.filter(author=self.request.user)

class UserCommentView(ListView):
	template_name='accounts/user_comments.html'
	context_object_name='comments'
	paginate_by=10

	def get_queryset(self):
		return Comment.objects.filter(user=self.request.user)




