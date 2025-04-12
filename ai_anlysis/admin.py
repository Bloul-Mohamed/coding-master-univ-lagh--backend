from django.contrib import admin
from .models import ProjectAnalysis


@admin.register(ProjectAnalysis)
class ProjectAnalysisAdmin(admin.ModelAdmin):
    list_display = ('project', 'idea_score', 'admin_approved',
                    'analysis_date', 'last_updated')
    list_filter = ('admin_approved', 'analysis_date')
    search_fields = ('project__title', 'improved_description')
    readonly_fields = ('analysis_date', 'last_updated')
    fieldsets = (
        (None, {
            'fields': ('project', 'admin_approved')
        }),
        ('Analysis Results', {
            'fields': ('improved_description', 'idea_score', 'suggestions')
        }),
        ('Timestamps', {
            'fields': ('analysis_date', 'last_updated'),
            'classes': ('collapse',)
        }),
    )
