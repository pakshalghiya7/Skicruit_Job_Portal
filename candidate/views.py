from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Profile,Skill,userSkill
from .forms import ProfileUpdateForm,SkillUpdateForm
# from django import form
from django.contrib.auth import get_user_model



# Create your views here.


# It displays the user profile and also the skills possessed by the user.
@login_required
def my_profile(request):
    you=request.user #Not User
    profile= Profile.objects.filter(user=you).first()
    skills=userSkill.objects.filter(user_skills=you)
    print(profile)
    if request.method== 'POST':
        form=SkillUpdateForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.user=you #Play here
            data.save()
            return redirect ('my-profile')
    else:
        form=SkillUpdateForm()
    context={
        "user":you,
        "data":profile,
        "skills":skills,
        "form":form,
        "profil_Page":"active",
    }
    return render(request,"candidate/profile.html",context)


#This function allows candidates to edit their profiles.
@login_required
def edit_profile(request):
    you=request.user
    profile = Profile.objects.filter(user=you).first()
    if request.method=='POST':
        form = ProfileUpdateForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            data=form.save(commit=False)
            data.user=you
            data.save()
            return redirect('my-profile')
    else:
        form=ProfileUpdateForm(instance=profile)
    context={
        "form":form,
        # "profile":profile ,  #Pass Profile and all and Try!

    }

    return render(request,'candidate/edit_profile.html',context)

@login_required
def profile_view_for_recruiter(request,pk): #Think about AutoSlug 
    # user=request.user
    profile=Profile.objects.filter(id=pk)
    user=profile.user
    profile_skills=userSkill.objects.get(user=user)
    context={
        "profile":profile,
        "profile_skills":profile_skills,

    }
    return render(request,"cabdidate/   .html",context)
 


        

