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
    path('<slug:slug>/',views.PostDetailView.as_view(),name='post-detail'),
    path('category/<slug:slug>/',views.CategoryDetailView.as_view(),name='category_list'),
    path('create-category/', views.CategoryCreateView.as_view(), name='create-category'),
    path('tag/<slug:slug>/',views.TagDetailView.as_view(),name='tag_list'),
    path('comment-edit/<int:pk>/',views.CommentUpdateView.as_view(),name='comment-edit'),
    path('subscribe/',views.subscribe,name='subscribe'),
    path('about/', views.about, name='about'),
]
