from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

app_name = "accounts"

urlpatterns = [
    # /accounts/signup/
    path('signup/', views.signup, name='signup'),

    # /accounts/logout/
    path('logout/', LogoutView.as_view(), name='logout'),

    # /accounts/login/
    path('login/', LoginView.as_view(
        template_name='accounts/login.html',
        redirect_authenticated_user=True
    ), name='login'),

    # /accounts/reset/
    path('reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),

    # /accounts/reset/done/
    path('reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),

    # /accounts/reset/<uidb64>/<token>/
    path('reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html',
        success_url=reverse_lazy('accounts:password_reset_complete')
    ), name='password_reset_confirm'),

    # /accounts/reset/complete/
    path('reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
