# from django.urls import path
# from . import views
# urlpatterns = [
#     # path('', views.home, name='home'),
#     path('', views.home_Candidate, name='candidate-Home'),
#     path('profile/', views.my_profile, name='my-profile'),
#     path('profile/edit/', views.edit_profile, name='edit-profile'),
#     path('job/', views.job_search_list, name='job-search-list'),
#     path('job/<slug>',views.job_Details,name="job-details"),
#     path("profile/<slug>",views.profile_view_for_recruiter,name="profile-view"),
#     # path("delete_skills/",views.) 
#     path('job/<slug>/apply/', views.apply_The_Given_Job , name='apply-job'),
#     path('job/<slug>/save/', views.save_The_Given_Job ,name='save-job'),
#     path('saved_job_list/', views.saved_jobs, name='saved-Jobs'),
#     path('applied_job_list/', views.applied_jobs, name='applied-jobs'),
#     path('job/<slug>/remove/', views.remove_The_Given_Job, name='remove-job'),

    
# ]
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
   
]

