from django.contrib import admin
from .models import Job,Applicants,Selected


# Register your models here.
@admin.register(Job)
class AuthorAdmin(admin.ModelAdmin):
    pass
@admin.register(Applicants)
class AuthorAdmin(admin.ModelAdmin):
    pass

@admin.register(Selected)
class AuthorAdmin(admin.ModelAdmin):
    pass