from django.shortcuts import render, redirect, get_object_or_404,HttpResponseRedirect,HttpResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import JobPostForm, JobUpdateForm
from .models import Job, Applicants, Selected
from candidate.models import Profile
# from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
class HomeRecruiterView(LoginRequiredMixin, View):
    def get(self, request):
        context = {
            "rec_activae_page": "active",
            "rec_navbar": 1
        }
        return HttpResponse("Recruiter Home Page")
        
class AddJobView(LoginRequiredMixin, View):
    def get(self, request):
        form = JobPostForm()
        user = request.user
        context = {
            "form": form,
            "user": user,
            "add_job_page": "active",
            "rec_navbar": 1,
        }
        return render(request, "recruiter/add_job.html", context)
    
    def post(self, request):
        form = JobPostForm(request.POST)
        user = request.user
        if form.is_valid():
            data = form.save(commit=False)
            data.user = user
            form.save()
            return HttpResponse("Job added Successfully")
        else:
            context = {
                "form": form,
                "user": user,
                "add_job_page": "active",
                "rec_navbar": 1,
            }
            return render(request, "recruiter/add_job.html", context)

class EditJobView(LoginRequiredMixin, View):
    def get(self, request, slug):
        user = request.user
        job = get_object_or_404(Job, slug=slug)
        form = JobUpdateForm(instance=job)
        context = {
            'form': form,
            'rec_navbar': 1,
            'job': job,
        }
        return render(request, 'recruiter/edit_job.html', context)
    
    def post(self, request, slug):
        user = request.user
        job = get_object_or_404(Job, slug=slug)
        form = JobUpdateForm(request.POST, instance=job)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect('add-job-detail', slug)
        else:
            context = {
                'form': form,
                'rec_navbar': 1,
                'job': job,
            }
            return render(request, 'recruiter/edit_job.html', context)

class JobView(LoginRequiredMixin, View):
    def get(self, request, slug):
        job = get_object_or_404(Job, slug=slug)
        context = {
            "job": job,
            "rec_navbar": 1,
        }
        return render(request, "recruiter/view_job.html", context)

class ApplicantListView(LoginRequiredMixin, View):
    def get(self, request, slug):
        job = get_object_or_404(Job, slug=slug)
        applicants = Applicants.objects.filter(job=job).order_by("-applied_At")
        profiles = []
        for applicant in applicants:
            profile = Profile.objects.filter(user=applicant.applicant).first()
            profiles.append(profile)
        context = {
            'rec_navbar': 1,
            'profiles': profiles,
            'job': job,
        }
        return render(request, 'recruiter/applicant_list.html', context)

class SelectApplicantView(LoginRequiredMixin, View):
    def get(self, request, can_id, job_id):
        job = get_object_or_404(Job, slug=job_id)
        profile = get_object_or_404(Profile, slug=can_id)
        user = request.user
        selected, created = Selected.objects.get_or_create(applicant=profile, job=job)
        applicant = Applicants.objects.filter(job=job, applicant=user).first()
        applicant.delete()
        return HttpResponseRedirect('/hiring/job/{}/applicants'.format(job.slug))

class SelectedListView(LoginRequiredMixin, View):
    def get(self, request, slug):
        job = get_object_or_404(Job, slug=slug)
        selected = Selected.objects.filter(job=job).order_by('date_posted')
        profiles = []
        for applicant in selected:
            profile = Profile.objects.filter(user=applicant.applicant).first()
            profiles.append(profile)
        context = {
            'rec_navbar': 1,
            'profiles': profiles,
            'job': job,
        }
        return render(request, 'recruiter/selected_list.html', context)

class RemoveApplicantView(LoginRequiredMixin, View):
    def get(self, request, can_id, job_id):
        job = get_object_or_404(Job, slug=job_id)
        profile = get_object_or_404(Profile, slug=can_id)
        user = profile.user
        applicant = Applicants.objects.filter(job=job, applicant=user).first()
        applicant.delete()
        return HttpResponseRedirect('/hiring/job/{}/applicants'.format(job.slug))

# @login_required
# def all_jobs(request):
#     jobs = Job.objects.filter(recruiter=request.user).order_by('-date_posted')
#     paginator = Paginator(jobs, 5)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'manage_jobs_page': "active",
#         'jobs': page_obj,
#         'rec_navbar': 1,
#     }
#     return render(request, 'recruiters/job_posts.html', context)

# # @login_required
# # def search_candidates(request):
# #     profile_list = Profile.objects.all()
# #     profiles = []
# #     for profile in profile_list:
# #         if profile.resume and profile.user != request.user:
# #             profiles.append(profile)

# #     rec1 = request.GET.get('r')
# #     rec2 = request.GET.get('s')

# #     if rec1 == None:
# #         li1 = Profile.objects.all()
# #     else:
# #         li1 = Profile.objects.filter(location__icontains=rec1)

# #     if rec2 == None:
# #         li2 = Profile.objects.all()
# #     else:
# #         li2 = Profile.objects.filter(looking_for__icontains=rec2)

# #     final = []
# #     profiles_final = []

# #     for i in li1:
# #         if i in li2:
# #             final.append(i)

# #     for i in final:
# #         if i in profiles:
# #             profiles_final.append(i)

# #     paginator = Paginator(profiles_final, 20)
# #     page_number = request.GET.get('page')
# #     page_obj = paginator.get_page(page_number)
# #     context = {
# #         'search_candidates_page': "active",
# #         'rec_navbar': 1,
# #         'profiles': page_obj,
# #     }
# #     return render(request, 'recruiters/candidate_search.html', context)

# @login_required
# def search_candidates(request):
#     profile_list = Profile.objects.exclude(user=request.user).filter(resume__isnull=False)
    
#     rec1 = request.GET.get('loction')
#     rec2 = request.GET.get('type')

#     li1 = Profile.objects.all() if rec1 is None else Profile.objects.filter(location__icontains=rec1)
#     li2 = Profile.objects.all() if rec2 is None else Profile.objects.filter(looking_for__icontains=rec2)

#     final = li1.intersection(li2)
#     profiles_final = final.intersection(profile_list)

#     paginator = Paginator(profiles_final, 5)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     context = {
#         'search_candidates_page': "active",
#         'rec_navbar': 1,
#         'profiles': page_obj,
#     }
#     return render(request, 'recruiters/candidate_search.html', context)


class AllJobsView(LoginRequiredMixin, View):
    def get(self, request):
        jobs = Job.objects.filter(user=request.user).order_by('-posted_at')
        paginator = Paginator(jobs, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'manage_jobs_page': "active",
            'jobs': page_obj,
            'rec_navbar': 1,
        }
        return render(request, 'recruiter/job_post.html', context)

class SearchCandidatesView(LoginRequiredMixin, View):
    def get(self, request):
        profile_list = Profile.objects.exclude(user=request.user).filter(resume__isnull=False)
        
        rec1 = request.GET.get('location')
        rec2 = request.GET.get('type')

        li1 = Profile.objects.all() if rec1 is None else Profile.objects.filter(location__icontains=rec1)
        li2 = Profile.objects.all() if rec2 is None else Profile.objects.filter(looking_for__icontains=rec2)

        final = li1.intersection(li2)
        profiles_final = final.intersection(profile_list)

        paginator = Paginator(profiles_final, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'search_candidates_page': "active",
            'rec_navbar': 1,
            'profiles': page_obj,
        }
        return render(request, 'recruiters/candidate_search.html', context)










