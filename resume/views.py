# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Application

def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        cover_letter = request.POST.get("cover_letter")
        resume_pdf = request.FILES.get("resume_pdf")

        # Save application
        Application.objects.create(
            job=job,
            name=name,
            email=email,
            phone=phone,
            cover_letter=cover_letter,
            resume_pdf=resume_pdf
        )
        return redirect("application_success")  # define this view

    return render(request, "resume/apply.html", {"job": job})
