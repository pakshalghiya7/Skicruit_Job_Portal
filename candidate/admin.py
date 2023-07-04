from django.contrib import admin
from candidate.models import Profile,Skill,UserSkill,Experience

# Register your models here.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(UserSkill)
admin.site.register(Experience)
