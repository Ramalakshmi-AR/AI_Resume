from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from .models import Job, Application
from .utils import match_resume_to_jobs


def upload_resume(request):
    results = []

    if request.method == 'POST':
        resume_text = request.POST.get('resume_text', '')
        jobs = Job.objects.all()
        matched_jobs = match_resume_to_jobs(resume_text, jobs)

        for job, score, matched, missing in matched_jobs:
            suggestion = f"Consider highlighting skills: {', '.join(missing)}" if missing else "Great match!"
            results.append((job, score, matched, missing, suggestion))

        results = sorted(results, key=lambda x: x[1], reverse=True)

    return render(request, 'resume/upload.html', {'results': results})


def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    return render(request, 'resume/job_detail.html', {'job': job})


def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        application = Application.objects.create(
            job=job,
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            cover_letter=request.POST.get('cover_letter'),
            resume_pdf=request.FILES.get('resume_pdf')
        )

        # Email confirmation
        send_mail(
            subject='Application Submitted Successfully',
            message=f'Thank you {application.name} for applying to {job.title}. We will contact you soon.',
            from_email=None,  # uses DEFAULT_FROM_EMAIL
            recipient_list=[application.email],
        )

        return redirect('apply_success')

    return render(request, 'resume/apply.html', {'job': job})


def apply_success(request):
    return render(request, 'resume/apply_success.html')
