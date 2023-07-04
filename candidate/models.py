from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from recruiter.models import Job
from autoslug import AutoSlugField
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from datetime import date
from django.core.exceptions import ValidationError

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True,
                                related_name="Profile")
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    country = CountryField(null=True, blank=True)
    location = models.CharField(
        max_length=50, null=True, blank=True, verbose_name='City')
    resume = models.FileField(upload_to='resumes', validators=[
                              FileExtensionValidator(allowed_extensions=['pdf', 'docx'])])
    profile_photo = models.FileField(upload_to="profile_Photo", validators=[
                                     FileExtensionValidator(allowed_extensions=['jpg', 'png'])])
    resume = models.FileField(upload_to='resumes')
    email = models.EmailField(max_length=50, null=True)
    passing_year = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(date.today().year - 1)])
    CHOICES = (
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Internship', 'Internship'),
        ('Remote', 'Remote'),
    )

    looking_for = models.CharField(
        choices=CHOICES, default="Full Time", max_length=30)
    bio = models.TextField(max_length=500, blank=True)
    experience = models.IntegerField(verbose_name="Experience In Years")
    slug = AutoSlugField(populate_from='user',
                         unique=True, null=True, blank=True)

    def clean(self): 
        current_year = date.today().year
        if self.passing_year > current_year - 1:
            raise ValidationError(
                "Passing year cannot be in the future or the current year.")
        if self.experience < 0:
            raise ValidationError("Experience cannot be negative.")
        if current_year - self.passing_year < self.experience:
            raise ValidationError(
                "Experience cannot be greater than the years since passing.")

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return "/profile/{}".format(self.slug)


class Skill(models.Model):
    skills = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.skills


class UserSkill(models.Model):
    user_skills = models.ForeignKey(
        User, related_name="user_skills", on_delete=models.CASCADE)
    skills = models.ForeignKey(Skill, on_delete=models.CASCADE)

    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    proficiency_level = models.CharField(
        max_length=12, choices=PROFICIENCY_CHOICES, default="Beginner")

    def __str__(self):
        return self.user_skills.username


class savedJobs(models.Model):
    job = models.ForeignKey(
        Job, related_name="saved_Jobs", on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="Saved_User", on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now=True)

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


class Experience(models.Model):
    user = models.ForeignKey(
        User, related_name="experiences", on_delete=models.CASCADE)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    company = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.position} at {self.company}"

    def calculate_duration(self):
        if self.end_date:
            duration = self.end_date - self.start_date
            years = duration.days // 365
            months = (duration.days % 365) // 30
            return f"{years}Y {months}M"
        else:
            return "Currently Working"

    def yearStart(self):
        return self.start_date.strftime('%y')

    def yearEnd(self):
        if (self.end_date is None):
             return self.start_date.strftime('%y')
        
        else:
            return self.end_date.strftime('%y')

    def monthStart(self):
        return self.start_date.strftime('%B')

    def monthEnd(self):
        if (self.end_date is None):
             return self.start_date.strftime('%B')
        
        else:
            return self.end_date.strftime('%B')

    def save(self, *args, **kwargs):
        self.duration = self.calculate_duration()
        super().save(*args, **kwargs)
    
