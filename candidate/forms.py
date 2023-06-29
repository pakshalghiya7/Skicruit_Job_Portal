from django.forms import ModelForm
from .models import Profile,Skill,userSkill,Experience

#Widgets and Validation  Add Karva
class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        exclude=["user","slug"]
class SkillUpdateForm(ModelForm):
    class Meta:
        model = userSkill
        exclude=["user_skills"]
        

class ExperienceForm(ModelForm):

    class Meta:
        model = Experience

        exclude = ['user']

# fields = ['company_name', 'job_title', 'start_date', 'end_date', 'description']