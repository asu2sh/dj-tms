from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

from .views import RegisterUserView, TaskViewSet, ReportGenerationView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('generate_report/', ReportGenerationView.as_view(), name='generate_report'),
]

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)

urlpatterns += router.urls
