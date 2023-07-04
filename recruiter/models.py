from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from autoslug import AutoSlugField
# Create your models here.

def validate_salary(value):
    if value < 0 or value > 1000:
        raise models.ValidationError("Salary must be between 0 and 1000 Lacs per Annum.")
    
class Job(models.Model): 
    user = models.ForeignKey(
        User, related_name="Job_Posting", on_delete=models.CASCADE)
    company = models.CharField(max_length=50)
    about_company = models.TextField()
    title = models.CharField(max_length=50)
    job_description = models.TextField()
    CHOICES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    )
    type = models.CharField(
        max_length=30, choices=CHOICES, default='Full Time', null=True)
    country = CountryField()
    city=models.CharField(max_length=50,null=True)
    skills = models.ForeignKey("candidate.Skill", related_name="Job_Skills", on_delete=models.CASCADE,null=True)
    salary = models.DecimalField(max_digits=5, decimal_places=2, validators=[validate_salary],help_text="In Lacs/Annum")
    no_of_openings = models.IntegerField()
    posted_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)

    def __str__(self):
        return self.title
    

class Applicants(models.Model):
    job = models.ForeignKey(
        Job, related_name="Applicants", on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name="Applied", on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.applicant.username


class Selected(models.Model):
    job = models.ForeignKey(
        Job, related_name='Selected_job', on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name='Selected_applicant', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.applicant.username
    
