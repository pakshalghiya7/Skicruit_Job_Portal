from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, HttpResponse
from .models import CustomUser
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin



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


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')
