from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectAnalysisViewSet

router = DefaultRouter()
router.register(r'analyses', ProjectAnalysisViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
