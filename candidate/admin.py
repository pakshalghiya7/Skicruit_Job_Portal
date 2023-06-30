from django.contrib import admin
from candidate.models import Profile,Skill,userSkill,Experience

# Register your models here.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(userSkill)
admin.site.register(Experience)
