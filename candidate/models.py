from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from recruiter.models import Job
from autoslug import AutoSlugField

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,
                                related_name="Profile")  # On_...Different Approaches
    first_Name = models.CharField(max_length=50)
    middle_Name = models.CharField(max_length=50)
    last_Name = models.CharField(max_length=50)
    country = CountryField()
    location = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='City')
    resume = models.FileField(upload_to='resumes')
    profile_Photo = models.FileField(
        upload_to="profile_Photo")  # Can make Default
    passing_year = models.IntegerField()
    CHOICES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    )

    looking_for = models.CharField(
        choices=CHOICES, default="Full Time", max_length=30)
    experience = models.IntegerField(verbose_name="Experience In Years")
    slug = AutoSlugField(populate_from='user', unique=True)

    # SlugField <-Think
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return "/profile/{}".format(self.slug)



class Skill(models.Model):
    skills = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.skills


class userSkill(models.Model):
    user_skills = models.ForeignKey(
        User, related_name="user_skills", on_delete=models.CASCADE)
    skills = models.ForeignKey(Skill, on_delete=models.CASCADE)


class savedJobs(models.Model):
    job = models.ForeignKey(
        Job, related_name="saved_Jobs", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="Saved_User", on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now=True)
    # review_Application_Field

    def __str__(self):
        return self.job.title
    
class appliedJobs(models.Model):
    job = models.ForeignKey(
        Job, related_name="applied_Jobs", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="applied_User", on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.job.title
