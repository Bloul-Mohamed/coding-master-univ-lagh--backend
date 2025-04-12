from django.contrib import admin
from .models import GuidanceAuthority, Interfaces


@admin.register(GuidanceAuthority)
class GuidanceAuthorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'university_name', 'email', 'sent_deadline')
    search_fields = ('name', 'university_name', 'email')


@admin.register(Interfaces)
class InterfacesAdmin(admin.ModelAdmin):
    list_display = ('interface_role', 'university_name',
                    'guidance_authority', 'email')
    list_filter = ('interface_role', 'university_name')
    search_fields = ('university_name', 'email')
