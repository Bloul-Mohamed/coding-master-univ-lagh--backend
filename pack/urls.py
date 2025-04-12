from django.urls import path
from . import views

app_name = 'pack'

urlpatterns = [
    path('send-email/<int:user_id>/',
         views.send_email_to_user, name='send_email_to_user'),
    path('send-bulk-email/', views.send_bulk_email, name='send_bulk_email'),
]
