from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from .forms import JobPostForm,JobUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Job
# Create your views here.

@login_required
def home_Recruiter(request):
    context={
        "rec_activae_page":"active",
        "rec_navbar":1
    }
    # return render(request,"recruiter/.html",context)
    return HttpResponse("Recruiter Home Page")
    # return render(request,"recruiter/ .html",context)

@login_required
def add_Job(request):
    user=request.user
    if request.method=='POST':
        form = JobPostForm(request.POST)
        if form.is_valid():
            data=form.save(commit=False)
            data.user=user
            form.save()
            return HttpResponse("Job added Successfully")
    else:
        form=JobPostForm()
    context={
        "form":form,
        "user":user,
        "add_job_page":"active",
        "rec_navbar":1,
                }
    return render(request,"recruiter/add_job.html",context)



@login_required
def edit_job(request, pk):
    user = request.user
    job = get_object_or_404(Job, id=pk)
    if request.method == "POST":
        form = JobUpdateForm(request.POST, instance=job)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect('add-job-detail', id)
    else:
        form = JobUpdateForm(instance=job)
    context = {
        'form': form,
        'rec_navbar': 1,
        'job': job,
    }
    return render(request, 'recruiters/   .html', context)


@login_required
def job_view(request,pk):
    job=get_object_or_404(Job,id=pk)
    context={
        "job":job,
        "rec_navbar":1,
    }
    return render (request,"recruiter/   .html",context)