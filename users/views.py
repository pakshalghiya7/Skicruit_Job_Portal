from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
def login(request):
    return render(request,'users/login.html')

def signup(request):
    return render(request,'users/signup.html')

@login_required
def account(request):
    context={'account_page': 'active'}
    return render(request,"users/account.html",context)
    
