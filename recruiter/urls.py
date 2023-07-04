from django.urls import path
from . import views
urlpatterns = [
    path('', views.HomeRecruiterView.as_view(), name='detail-recruiters'),
    path('job/add', views.AddJobView.as_view(), name='add-job'),
    path('job/<slug>', views.JobView.as_view(), name='add-job-detail'),
    path('job/<slug>/edit/', views.EditJobView.as_view(), name='edit-job-post'),
    path('job/<slug>/applicants', views.ApplicantListView.as_view(), name='applicant-list'),
    path('job/<int:job_id>/select-applicant/<int:can_id>/', views.SelectApplicantView.as_view(), name='select-applicant'),
    path('job/<int:job_id>/remove-applicant/<int:can_id>/', views.RemoveApplicantView.as_view(), name='remove-applicant'),
    path('job/<slug>/selected', views.SelectedListView.as_view(), name='selected-list'),
    path('jobs/', views.AllJobsView.as_view(), name='job-list'),
    path('candidates/search', views.SearchCandidatesView.as_view(), name='search-candidates'),

]

