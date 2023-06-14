from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField

# Create your models here.


class Job(models.Model):
    user = models.ForeignKey(
        User, related_name="Job_Posting", on_delete=models.CASCADE)
    company = models.CharField(max_length=50)
    about_Company = models.TextField()
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
  #  City or Location=models.CharField(max_length=50) Django_Cities
    skills_required = models.CharField(max_length=50)
    salary = models.IntegerField(help_text="In Lacs/Annum")
    no_Of_Opening = models.IntegerField()
    posted_At = models.DateTimeField(auto_now=True)
    updated_At = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Applicants(models.Model):
    job = models.ForeignKey(
        Job, related_name="Applicants", on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name="Applied", on_delete=models.CASCADE)
    applied_At = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.applicant


class Selected(models.Model):
    job = models.ForeignKey(
        Job, related_name='Selected_job', on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name='Selected_applicant', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.applicant
    
