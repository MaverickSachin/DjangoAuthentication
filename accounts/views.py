from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from .forms import SignUpForm
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetCompleteView
)


def signup(request):
    if request.user.is_authenticated:
        return redirect('tutorial:index')
    else:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('tutorial:index')
        else:
            form = SignUpForm()

        context = {'form': form, 'title': 'Sign Up'}
        return render(request, 'accounts/signup.html', context=context)


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('accounts:password_reset_done')
    email_template_name = 'accounts/password_reset_email.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tutorial:index')
        else:
            return super().dispatch(*args, **kwargs)


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset_done.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tutorial:index')
        else:
            return super().dispatch(*args, **kwargs)


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset_complete.html'

    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tutorial:index')
        else:
            return super().dispatch(*args, **kwargs)
