from django.shortcuts import render,redirect
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .forms import CreateUserForm,ProfileUpdateForm,UserUpdateForm
from .models import Profile
from posts.models import Post

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
	success_url = reverse_lazy('posts:all_posts')

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
			return redirect('posts:all_posts')
		return super(RegisterPage, self).get(*args, **kwargs)

def user_profile(request):
	posts=Post.objects.filter(author=request.user)
	p_form=ProfileUpdateForm()
	u_form=UserUpdateForm()
	context={'posts':posts,'title':f"{request.user}'s Profile",'u_form':u_form,'p_form':p_form}
	return render(request,'accounts/user_profile.html',context)

class UserPostView(ListView):
	template_name='accounts/user_posts_edit.html'
	context_object_name='posts'
	paginate_by=10

	def get_queryset(self):
		return Post.objects.filter(author=self.request.user)



