from django.db import models


class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    skills = models.TextField(help_text="Comma separated skills")

    def __str__(self):
        return self.title


class Resume(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to='resumes/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class Application(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cover_letter = models.TextField(blank=True)
    resume_pdf = models.FileField(upload_to='resumes/', null=True, blank=True)
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.job.title}"