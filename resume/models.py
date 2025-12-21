# models.py
from django.db import models

class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cover_letter = models.TextField(blank=True)
    resume_pdf = models.FileField(upload_to="resumes/")
    applied_at = models.DateTimeField(auto_now_add=True)
