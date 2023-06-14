from .models import Job,Selected,Applicants
from django.forms import ModelForm

class JobPostForm(ModelForm):
    class Meta:
        model = Job
        exclude=["user","Posted_At","Updated_At"]
        help_texts = {
            'skills_req': 'Enter all the skills required each separated by commas.',
            }

class JobUpdateForm(ModelForm):
    class Meta:
        model = Job
        exclude=["User","Posted_At","Updated_At"]
        help_texts = {
            'skills_req': 'Enter all the skills required each separated by commas.',
            }


