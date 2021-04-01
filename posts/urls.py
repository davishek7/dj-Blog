from django.urls import path,include
from . import views

app_name='posts'

urlpatterns = [
    path('',views.PostList.as_view(),name='all_posts'),
    path('create-post/',views.PostCreateView.as_view(),name='create-post'),
    path('update-post/<slug:slug>/',
         views.PostUpdateView.as_view(), name='update-post'),
    path('delete-post/<slug:slug>/',
         views.PostDeleteView.as_view(), name='delete-post'),
    path('posts/<slug:slug>/',views.post_detail,name='post_detail'),
    path('category/<slug:category_slug>/',views.category_list,name='category_list'),
    path('about/', views.about, name='about'),
]
