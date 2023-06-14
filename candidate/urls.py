from django.urls import path
from . import views
urlpatterns = [
    path('profile/', views.my_profile, name='my-profile'),
    path('profile/edit/', views.edit_profile, name='edit-profile'),
    
]

