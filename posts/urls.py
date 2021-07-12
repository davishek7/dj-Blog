from django.urls import path
from . import views

app_name='posts'

urlpatterns = [
    path('',views.PostList.as_view(),name='all-posts'),
    path('create-post/',views.PostCreateView.as_view(),name='create-post'),
    path('update-post/<slug:slug>/',
         views.PostUpdateView.as_view(), name='update-post'),
    path('delete-post/<slug:slug>/',
         views.PostDeleteView.as_view(), name='delete-post'),
    path('search/', views.search, name='search'),
    path('posts/<slug:slug>/',views.post_detail,name='post-detail'),
    path('category/<slug:category_slug>/',views.category_list,name='category_list'),
    path('create-category/', views.CategoryCreateView.as_view(), name='create-category'),
    path('comment-edit/<int:pk>/',views.CommentUpdateView.as_view(),name='comment-edit'),
    path('subscribe/',views.subscribe,name='subscribe'),
    path('about/', views.about, name='about'),

]
