from django.urls import path
from . import views
urlpatterns = [
    path('', views.home_Recruiter, name='detail-recruiters'),
    path('job/add', views.add_Job, name='add-job'),
    # path('job/<int:id>/edit/', views.edit_Job, name='edit-job-post'),
    path('job/<int:pk>', views.job_view, name='add-job-detail'),
    # path('jobs/', views.all_jobs, name='job-list'),
    
]
 