from django.urls import path
from . import views

app_name = 'pack'

urlpatterns = [
    # Regular views for templates
    path('send-email/<int:user_id>/',
         views.send_email_to_user, name='send_email_to_user'),
    path('send-bulk-email/', views.send_bulk_email, name='send_bulk_email'),

    # API endpoints (for Swagger documentation)
    path('api/send-email/<int:user_id>/',
         views.send_email_to_user_api, name='send_email_to_user_api'),
    path('api/send-bulk-email/', views.send_bulk_email_api,
         name='send_bulk_email_api'),
]
