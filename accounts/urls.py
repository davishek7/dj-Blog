from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.user_profile, name='user-profile'),
    path('user-posts/',views.UserPostView.as_view(),name='user-posts'),
    path('comments/', views.UserCommentView.as_view(), name='comments'),
]
