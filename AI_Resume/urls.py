from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse

def home(request):
    return HttpResponse("AI-Resume is Running")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),               # Homepage
    path('resume/', include('resume.urls')),   # All resume-related URLs prefixed with /resume/
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
