from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from .models import Profile, Skill, UserSkill, Experience
from .forms import ProfileUpdateForm, SkillUpdateForm, ExperienceForm
from recruiter.models import Job, Selected, Applicants
from candidate.models import savedJobs, appliedJobs
from users.models import CustomUser


class HomeView(View):
    def get(self, request):
        return render(request, "candidate/home.html")


class HomeCandidateView(View):
    def get(self, request):
        context = {"home_page": 'active'}
        return render(request, "candidate/candidate_Home.html", context)

class CandidateDetailsView(View):
    def get(self,request):
        return render(request, "candidate/details.html")

class MyProfileView(LoginRequiredMixin, View):
    def get(self, request):
        you = request.user
        profile = Profile.objects.filter(user=you).first()
        skills = UserSkill.objects.filter(user_skills=you)
        experience = Experience.objects.filter(user=you)
        # print(CustomUser.objects.filter(email=you))
        # print(you.username)
        skill_form = SkillUpdateForm()
        experience_form = ExperienceForm()
        context = {
            "user": you,
            "data": profile,
            "skills": skills,
            "skill_form": skill_form,
            "experience": experience,
            "experience_form": experience_form,
            "profile_Page": "active",
        }
        return render(request, "candidate/profile.html", context)

    def post(self, request):
        you = request.user
        skill_form = SkillUpdateForm(request.POST)
        experience_form = ExperienceForm(request.POST)
        if skill_form.is_valid():
            data = skill_form.save(commit=False)
            data.user_skills = you
            data.save()
            return redirect('my-profile')
        if experience_form.is_valid():
            data = experience_form.save(commit=False)
            data.user = you
            data.save()
            return redirect('my-profile')
        else:
            profile = Profile.objects.filter(user=you).first()
            skills = UserSkill.objects.filter(user_skills=you)
            experience = Experience.objects.filter(user=you)

            context = {
                "user": you,
                "data": profile,
                "skills": skills,
                "skill_form": skill_form,
                "experience": experience,
                "experience_form": experience_form,
                "profile_Page": "active",
            }
            return render(request, "candidate/profile.html", context)


class EditProfileView(LoginRequiredMixin, View):
    def get(self, request):
        you = request.user
        profile = Profile.objects.filter(user=you).first()
        form = ProfileUpdateForm(instance=profile)
        context = {
            "form": form,
        }
        return render(request, 'candidate/edit_profile.html', context)

    def post(self, request):
        you = request.user
        profile = Profile.objects.filter(user=you).first()
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = you
            data.save()
            return redirect('my-profile')
        else:
            context = {
                "form": form,
            }
            return render(request, 'candidate/edit_profile.html', context)


class ProfileViewForRecruiterView(LoginRequiredMixin, View):
    def get(self, request, pk):
        profile = Profile.objects.filter(user=pk)
        print(profile)
        user = profile.user
        profile_skills = UserSkill.objects.get(user=user)
        context = {
            "profile": profile,
            "profile_skills": profile_skills,
        }
        return render(request, "candidate/profile.html", context)


class JobSearchListView(LoginRequiredMixin, View):
    def get(self, request):
        search_query = request.GET.get("query")
        search_location = request.GET.get("location")
        query_list = []
        if search_query is None:
            job = Job.objects.all()
        else:
            find_title = Job.objects.filter(
                title__icontains=search_query).order_by("-posted_at")
            find_company = Job.objects.filter(
                company__icontains=search_query).order_by("-posted_at")
            find_type = Job.objects.filter(
                type__icontains=search_query).order_by("-posted_at")
            find_skills = Job.objects.filter(
                skills__skills__icontains=search_query).order_by("-posted_at")

            for i in find_title:
                query_list.append(i)
            for i in find_company:
                query_list.append(i)
            for i in find_type:
                query_list.append(i)
            for i in find_skills:
                query_list.append(i)

        if search_location is None:
            locat = Job.objects.all()
        else:
            locat = Job.objects.filter(
                country__icontains=search_location).order_by("-posted_at")

        final_query_list = []
        for i in query_list:
            if i in locat:
                final_query_list.append(i)

        paginator = Paginator(final_query_list, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'jobs': page_obj,
            'query': search_query,
        }
        return render(request, 'candidate/job_search_list.html', context)

class SavedJobsView(LoginRequiredMixin, View):
    def get(self, request):
        jobs = savedJobs.objects.filter(
            user=request.user).order_by('-posted_at')
        return render(request, 'candidate/saved_Job.html', {'jobs': jobs, 'candidate_navbar': 1})


class AppliedJobsView(LoginRequiredMixin, View):
    def get(self, request):
        jobs = appliedJobs.objects.filter(
            user=request.user).order_by('-posted_at')
        statuses = []
        for job in jobs:
            if Selected.objects.filter(job=job.job).filter(applicant=request.user).exists():
                statuses.append(0)
            elif Applicants.objects.filter(job=job.job).filter(applicant=request.user).exists():
                statuses.append(1)
            else:
                statuses.append(2)
        zipped = zip(jobs, statuses)
        return render(request, 'candidate/applied_Jobs.html', {'zipped': zipped, 'candidate_navbar': 1})


class SaveJobView(LoginRequiredMixin, View):
    def get(self, request, slug):
        user = request.user
        job = get_object_or_404(Job, slug=slug)
        saved_Job, created = savedJobs.objects.get_or_create(
            job=job, user=user)
        return HttpResponseRedirect('/job/{}'.format(job.slug))


class ApplyJobView(LoginRequiredMixin, View):
    def get(self, request, slug):
        user = request.user
        job = get_object_or_404(Job, slug=slug)
        applied_Job, created = appliedJobs.objects.get_or_create(
            job=job, user=user)
        applicants, creation = Applicants.objects.get_or_create(
            job=job, applicant=user)
        return HttpResponseRedirect('/job/{}'.format(job.slug))


class RemoveJobView(LoginRequiredMixin, View):
    def get(self, request, slug):
        user = request.user
        job = get_object_or_404(Job, slug=slug)
        saved_job = savedJobs.objects.filter(job=job, user=user).first()
        saved_job.delete()
        return HttpResponseRedirect('/job/{}'.format(job.slug))


class JobDetailsView(LoginRequiredMixin, View):
    def get(self, request, slug):
        user = request.user
        profile = Profile.objects.filter(user=user).first()
        job = get_object_or_404(Job, slug=slug)
        applied_button, saved_button = 0, 0
        if appliedJobs.objects.filter(user=user).filter(job=job).exists():
            applied_button = 1
        if savedJobs.objects.filter(user=user).filter(job=job).exists():
            saved_button = 1
        relevant_jobs = []
        jobs1 = Job.objects.filter(
            company__icontains=job.company).order_by('-posted_at')
        jobs2 = Job.objects.filter(
            type__icontains=job.type).order_by('-posted_at')
        jobs3 = Job.objects.filter(
            title__icontains=job.title).order_by('-posted_at')
        for i in jobs1:
            if len(relevant_jobs) > 5:
                break
            if i not in relevant_jobs and i != job:
                relevant_jobs.append(i)
        for i in jobs2:
            if len(relevant_jobs) > 5:
                break
            if i not in relevant_jobs and i != job:
                relevant_jobs.append(i)
        for i in jobs3:
            if len(relevant_jobs) > 5:
                break
        if i not in relevant_jobs and i != job:
            relevant_jobs.append(i)

        context = {
            'job': job,
            'profile': profile,
            'applied_button': applied_button,
            'saved_button': saved_button,
            'candidate_navbar': 1,
            'relevant_jobs': relevant_jobs,
        }
        return render(request, 'candidate/job_details.html', context)


class DeleteSkillView(LoginRequiredMixin, View):
    def post(self, request, pk=None):
        id_list = request.POST.getlist('choices')
        id_list1 = []
        for skill_id in id_list:
            id1 = Skill.objects.get(skills=skill_id).id
            id_list1.append(id1)
        for ids in id_list1:
            UserSkill.objects.get(skills=ids).delete()

        return redirect('my-profile')
