from django.contrib import admin
from candidate.models import Profile,Skill,userSkill

# Register your models here.
admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(userSkill)
