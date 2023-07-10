from django.forms import ModelForm
from .models import Profile, Skill, UserSkill, Experience

class ProfileUpdateForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ["user","email" "slug"]


class SkillUpdateForm(ModelForm):
    class Meta:
        model = UserSkill
        exclude = ["user_skills"]


class ExperienceForm(ModelForm):

    class Meta:
        model = Experience
        exclude = ['user']
