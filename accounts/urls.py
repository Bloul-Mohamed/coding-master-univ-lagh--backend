from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GuidanceAuthorityViewSet, InterfacesViewSet

router = DefaultRouter()
router.register(r'guidance-authorities', GuidanceAuthorityViewSet)
router.register(r'interfaces', InterfacesViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
