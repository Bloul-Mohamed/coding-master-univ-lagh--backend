from django.contrib import admin
from .models import Project, Student


class StudentInline(admin.TabularInline):
    model = Student
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'guidance_authority',
                    'send_date', 'is_complete')
    list_filter = ('status', 'guidance_authority', 'is_complete')
    search_fields = ('title', 'description', 'email')
    inlines = [StudentInline]


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email',
                    'project', 'university_name', 'field_of_study', 'branch',
                    'user_id', 'uuid', 'establishment_id')
    list_filter = ('university_name', 'country', 'field_of_study', 'branch')
    search_fields = ('first_name', 'last_name', 'email',
                     'field_of_study', 'branch', 'user_id', 'uuid',
                     'id_individual', 'establishment_id', 'user_name')
