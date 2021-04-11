from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('user-posts/',views.UserPostView.as_view(),name='user-posts'),
    path('comments/', views.UserCommentView.as_view(), name='comments'),
]
