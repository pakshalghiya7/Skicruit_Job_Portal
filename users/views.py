from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse


# Create your views here.

@login_required
def account(request):
    context = {'account_page': 'active'}
    return render(request, "users/account.html", context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user_type = request.POST.get('user_type')

        if CustomUser.objects.filter(username=username).exists() or CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Username or email already exists. Please choose a different one.')
            return redirect(reverse('signup') + f'?user_type={user_type}')

        if user_type == 'employee':
            user = CustomUser.objects.create_user(
                username=username, email=email, password=password, is_employee=True)
        else:
            user = CustomUser.objects.create_user(
                username=username, email=email, password=password, is_employee=False)

        return redirect('home')

    user_type = request.GET.get("user_type")
    context = {
        "user_type": user_type,
    }
    return render(request, 'users/signup.html', context)


def loginview(request):    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        # print(user)
        if user is None:
            messages.error(request, 'Invalid login credentials. Please try again.')

            return render(request, 'users/login.html')  # Message

        if user.is_employee is True :

            login(request, user)
            return redirect('home1')
        elif user.is_employee is False:
            login(request, user)
            return redirect('detail-recruiters')
      
    return render(request, 'users/login.html')



