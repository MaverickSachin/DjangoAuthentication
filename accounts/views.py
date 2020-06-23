from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignUpForm


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
