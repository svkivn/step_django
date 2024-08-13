from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

from accounts.forms import UserCreateForm

# 1
def signupaccount(request):
    if request.method == 'GET':
        return render(request, 'accounts/signupaccount.html', {'form': UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
            user.save()
            login(request, user)
            return redirect("home-view")
        else:
            return render(request, 'accounts/signupaccount.html',
                          {'form': UserCreationForm, 'error': 'Passwords do not match'})
