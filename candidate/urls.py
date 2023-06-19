from django.urls import path
from . import views
urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.home_Candidate, name='candidate-Home'),
    path('profile/', views.my_profile, name='my-profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    path('job/', views.job_search_list, name='job-search-list'),
    
]

