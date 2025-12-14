from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'skills')
    search_fields = ('title', 'skills')

    
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job', 'applied_at')
    search_fields = ('name', 'email', 'job__title')
    list_filter = ('job',)

