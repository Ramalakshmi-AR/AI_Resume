from django.shortcuts import render, get_object_or_404, redirect
from .models import Job, Application
from .utils import match_resume_to_jobs
from django.http import HttpResponse




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
        try:
            resume_file = request.FILES.get('resume_pdf')

            # Ensure media/resumes folder exists
            import os
            from django.conf import settings
            resumes_path = os.path.join(settings.MEDIA_ROOT, 'resumes')
            if not os.path.exists(resumes_path):
                os.makedirs(resumes_path)
                Application.objects.create(
                job=job,
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                cover_letter=request.POST.get('cover_letter'),
                resume_pdf=resume_file
            )

        except Exception as e:
            # Show exact error on page for debugging
            return HttpResponse(f"<h2>Error occurred:</h2><pre>{e}</pre>")

        return redirect('apply_success')

    return render(request, 'resume/apply.html', {'job': job})

def apply_success(request):
    return render(request, 'resume/apply_success.html')
