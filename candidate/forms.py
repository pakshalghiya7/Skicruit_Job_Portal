from django.forms import ModelForm
from .models import Profile,Skill,userSkill

#Widgets and Validation  Add Karva
class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        exclude=["user","slug"]
class SkillUpdateForm(ModelForm):
    class Meta:
        model = userSkill
        fields= '__all__'

 