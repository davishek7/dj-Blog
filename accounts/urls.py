from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('posts-edit/',views.UserPostView.as_view(),name='posts-edit'),
    path('comments-edit/', views.UserCommentView.as_view(), name='comments-edit'),
]
