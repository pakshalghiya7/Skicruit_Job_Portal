from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('', views.HomeCandidateView.as_view(), name='candidate-Home'),
    path('profile/', views.MyProfileView.as_view(), name='my-profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit-profile'),
    path('job/', views.JobSearchListView.as_view(), name='job-search-list'),
    path('job/<slug>', views.JobDetailsView.as_view(), name="job-details"),
    path("profile/<slug>", views.ProfileViewForRecruiterView.as_view(), name="profile-view"),
    path('job/<slug>/apply/', views.ApplyJobView.as_view(), name='apply-job'),
    path('job/<slug>/save/', views.SaveJobView.as_view(), name='save-job'),
    path('saved_job_list/', views.SavedJobsView.as_view(), name='saved-Jobs'),
    path('applied_job_list/', views.AppliedJobsView.as_view(), name='applied-jobs'),
    path('job/<slug>/remove/', views.RemoveJobView.as_view(), name='remove-job'),
    path('delete_skill/', views.DeleteSkillView.as_view(), name='skill-delete'),
    path('home/', views.CandidateDetailsView.as_view(), name='home1'),
]

