from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from accounts.views import RegisterPage,UserLoginView

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('secret/', admin.site.urls),
    path('',include('frontend.urls',namespace='frontend')),
    path('posts/',include('posts.urls',namespace='posts')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('login/', UserLoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('register/',RegisterPage.as_view(),name='register'),
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('summernote/', include('django_summernote.urls')),

    path('password-change/', auth_views.PasswordChangeView.as_view(
    	template_name='accounts/password_change.html'), name='password_change'),

    path('password-change-done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'), name='password_change_done'),

    path('reset-password/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name="password_reset"),

    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
         name="password_reset_confirm"),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),
         name="password_reset_complete"),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
