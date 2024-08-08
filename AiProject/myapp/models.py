
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_student = models.BooleanField(default=False)
    is_practitioner = models.BooleanField(default=False)

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Add additional fields specific to students here

class Practitioner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Add additional fields specific to practitioners here

class Recording(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    confession = models.FileField(upload_to='recordings/', null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

class StudyMaterial(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='study_materials/', null=True, blank=True)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Assignment(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='assignments/')
    practitioner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assignments')

    def __str__(self):
        return self.title

class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='submissions')
    file = models.FileField(upload_to='submissions/')
    grade = models.CharField(max_length=10, null=True, blank=True)
    notes = models.TextField(blank=True, null=True)  # Add this line

    def __str__(self):
        return f"Submission by {self.student.username} for {self.assignment.title}"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recording = models.ForeignKey(Recording, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'recording')

    def __str__(self):
        return f"{self.user.username} - {self.recording.title}"
