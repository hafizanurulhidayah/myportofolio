import uuid

from django.contrib.auth.models import User
from django.db import models


class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]

    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)
    experience_image_url = models.URLField(blank=True, max_length=500)
    starred_by = models.ManyToManyField(
        User, related_name="starred_experience", blank=True
    )

    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None

class ExperiencePhoto(models.Model):
    experience = models.ForeignKey(
        Experience,
        related_name='photos',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='experience_photos/')

class Education(models.Model):
    institution = models.CharField(max_length=100) 
    degree = models.CharField(max_length=100) 
    year = models.CharField(max_length=20)
    achievements = models.TextField()

class PreviousWork(models.Model):
    title = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    category = models.CharField(max_length=50)
    link = models.URLField(blank=True)
    photo = models.ImageField(
        upload_to="project_photos/",
        blank=True,
        null=True
    )



